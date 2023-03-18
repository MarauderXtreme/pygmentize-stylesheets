#!/usr/bin/env python3

from pprint import pprint
from itertools import tee, islice, chain
import re
import cssutils
import os

ci_run = os.getenv('CI_RUN')

if not ci_run:
    import pickle


def available_next(itrbl):
    """
    Splits an iterable into two streams
    i is the normal ordered iterable
    n is the next element from i
    """
    i, n = tee(itrbl, 2)
    n = chain(islice(n, 1, None), [None])
    return zip(i, n)

def pickle_cache(file):
    if ci_run:
        return False
    if os.path.isfile('cache/' + file + '.pcl'):
        pickle_file = open('cache/' + file + '.pcl', 'rb')
        return_value = pickle.load(pickle_file)
        pickle_file.close()
        return return_value
    else:
        return False

def pickle_caching(var, file):
    if ci_run:
        return
    pickle_file = open('cache/' + file + '.pcl', 'wb')
    pickle.dump(var, pickle_file)
    pickle_file.close()

def get_css_files(directory, suffix = ".css"):
    css_files = list()
    
    if directory[-1] != "/":
        directory = directory + "/"

    for file in os.listdir(directory):
        if file.endswith(suffix):
            css_files.append(directory + file)
    
    return sorted(css_files)

def get_css_classes(css_files):
    parser = cssutils.parse.CSSParser()
    classes = set()
    for file in css_files:
        sheet = parser.parseFile(file, validate = True)
        for i, n in available_next(sheet.cssRules):
            if i.type == 1 and n.type == 1001:
                classes.add((i.selectorText, None, n.cssText))
            elif i.type == 1 and n.type == 1:
                classes.add((i.selectorText, None, None))
    return sorted(list(classes))

def get_all_properties(class_list, css_files):
    parser = cssutils.parse.CSSParser()
    for index, t in enumerate(class_list):
        t = [t[0], set(), t[2]]
        for file in css_files:
            sheet = parser.parseFile(file, validate = True)
            for rule in sheet.cssRules:
                if rule.type == 1 and rule.selectorText == t[0]:
                    property_list = re.findall('.+:', rule.style.cssText)
                    t[1].update(property_list)
        class_list[index] = t
    return sorted(class_list)

def generate_highlight_css(properties):
    with open('dist/highlight.scss', 'w') as var_css:
        for extracted_rule in properties:
            var_string = ''
            for property in extracted_rule[1]:
                var_string = var_string + property + ' var(--' + extracted_rule[0].replace('.highlight', 'highlight').replace(' ', '').replace('.', '-').lower() + '-' + property.replace(':', '') + '); '
            if extracted_rule[2] is None:
                print(f"{extracted_rule[0]}{{ {var_string}}}", file=var_css)
            else:
                print(f"{extracted_rule[0]} {{ {var_string}}} {extracted_rule[2]}", file=var_css)

def structure_properties(properties):
    structure = dict()
    for rule in properties:
        css_property = dict()
        for property in rule[1]:
            property = property.replace(':', '')
            css_property[property] = "initial"
        if rule[2] is not None:
            css_property['comment'] = rule[2]

        structure[rule[0]] = css_property
    return structure

def generate_var_css(css_files, structured_properties):
    for file in css_files:
        parser = cssutils.parse.CSSParser()
        sheet = parser.parseFile(file, validate = True)
        for rule in sheet.cssRules:
            if rule.type == 1:
                selector = rule.selectorText
                css_text = re.findall('[^; \n]+: [^; ]+', rule.style.cssText)
                for property in css_text:
                    setting = property.split(':')[0]
                    variable = property.split(':')[1].replace(' ', '')
                    structured_properties[selector][setting] = variable
        var_list = list()
        for selector, properties in structured_properties.items():
            for property, value in properties.items():
                if property == "comment":
                    continue
                if 'comment' in structured_properties[selector]:
                    var_list.append("\t--" + selector.replace('.highlight', 'highlight').replace(' ', '').replace('.', '-').lower() + '-' + property + ": " + value + ";\t" + structured_properties[selector]['comment'])
                else:
                    var_list.append("\t--" + selector.replace('.highlight', 'highlight').replace(' ', '').replace('.', '-').lower() + '-' + property + ": " + value + ";")
        theme_name = file.split('/')[-1].replace('.css', '')
        with open('dist/themes/' + theme_name + '.scss', 'w') as var_css:
            print(f".{theme_name} {{", file=var_css)
            for line in sorted(var_list):
                print(f"{line}", file=var_css)
            print(f"}}", file=var_css)

css_files = pickle_cache('css_files')
if not css_files:
    css_files = get_css_files("css")
    pickle_caching(css_files, 'css_files')

all_classes = pickle_cache('all_classes')
if not all_classes:
    all_classes = get_css_classes(css_files)
    pickle_caching(all_classes, 'all_classes')

all_properties = pickle_cache('all_properties')
if not all_properties:
    all_properties = get_all_properties(all_classes, css_files)
    pickle_caching(all_properties, 'all_properties')

generate_highlight_css(all_properties)
generate_var_css(css_files, structure_properties(all_properties))
