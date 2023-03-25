#!/usr/bin/env python3

from itertools import tee, islice, chain
import re
import cssutils
import os


def available_next(itrbl):
    """
    Splits an iterable into two streams
    i is the normal ordered iterable
    n is the next element from i
    """
    i, n = tee(itrbl, 2)
    n = chain(islice(n, 1, None), [None])
    return zip(i, n)


def get_css_files(directory, suffix=".css"):
    css_files = list()
    if directory[-1] != "/":
        directory = directory + "/"
    for file in os.listdir(directory):
        if file.endswith(suffix):
            css_files.append(directory + file)
    return sorted(css_files)


def get_theme_list(files, suffix=".css"):
    themes = list()
    for theme in files:
        themes.append(theme.split("/")[-1].replace(suffix, ''))
    return sorted(themes)


def generate_include_all_mixins(themes):
    with open('dist/all-themes.scss', 'w') as all_mixins:
        print(f'@charset "utf-8";\n', file=all_mixins)
        for theme in themes:
            print(f"@import 'themes/{theme}';", file=all_mixins)


def generate_classes_for_all_themes(themes):
    with open('dist/all-themes-classes.scss', 'w') as all_classes:
        for theme in themes:
            print(f".{theme} {{", file=all_classes)
            print(f"\t@include {theme}-pygment;", file=all_classes)
            print(f"}}\n", file=all_classes)
    return sorted(themes)


def generate_basic_structure(files):
    structure = dict()
    parser = cssutils.parse.CSSParser()
    for file in files:
        sheet = parser.parseFile(file, validate=True)
        for i, n in available_next(sheet.cssRules):
            if i.type == 1:
                if i.selectorText not in structure:
                    structure[i.selectorText] = dict()
                property_list = re.findall(".+:", i.style.cssText)
                for property in property_list:
                    prop = property.replace(":", "")
                    if prop not in structure[i.selectorText]:
                        structure[i.selectorText][prop] = "initial"
            if i.type == 1 and n.type == 1001:
                if "comment" not in structure[i.selectorText]:
                    structure[i.selectorText]["comment"] = n.cssText
                elif structure[i.selectorText]["comment"] != n.cssText:
                    print("In " + file +
                          " the comment is " + n.cssText +
                          " instead of " + structure[i.selectorText]["comment"])
    return structure


def generate_highlight_scss(structure):
    with open("dist/highlight.scss", "w") as highlight:
        for selector, properties in structure.items():
            var_css_string = ""
            for property, value in properties.items():
                if property == "comment":
                    continue
                var_css_string = var_css_string + property + ": var(--" + selector.replace(
                    ".highlight", "highlight").replace(" ", "").replace(
                    ".", "-").lower() + "-" + property.replace(":", "") + "); "
            if "comment" in properties:
                print(
                    f"{selector} {{ {var_css_string}}} {properties['comment']}", file=highlight)
            else:
                print(f"{selector} {{ {var_css_string}}}", file=highlight)


def generate_var_css(css_files, structure, suffix=".css"):
    for file in css_files:
        parser = cssutils.parse.CSSParser()
        sheet = parser.parseFile(file, validate=True)
        generator_handle = structure
        for rule in sheet.cssRules:
            if rule.type == 1:
                selector = rule.selectorText
                css_text = re.findall('[^; \n]+: [^; ]+', rule.style.cssText)
                for property in css_text:
                    setting = property.split(':')[0]
                    variable = property.split(':')[1].replace(' ', '')
                    generator_handle[selector][setting] = variable
        var_list = list()
        for selector, properties in generator_handle.items():
            for property, value in properties.items():
                if property == "comment":
                    continue
                if "comment" in generator_handle[selector]:
                    var_list.append("--" + selector.replace('.highlight', 'highlight').replace(' ', '').replace(
                        '.', '-').lower() + '-' + property + ": " + value + ";\t" + generator_handle[selector]["comment"])
                else:
                    var_list.append("--" + selector.replace('.highlight', 'highlight').replace(
                        ' ', '').replace('.', '-').lower() + '-' + property + ": " + value + ";")
        theme_name = file.split('/')[-1].replace(suffix, '')
        with open('dist/themes/' + theme_name + '.scss', 'w') as var_scss:
            print(f"@mixin {theme_name}-pygment {{", file=var_scss)
            for line in sorted(var_list):
                print(f"\t{line}", file=var_scss)
            print(f"}}", file=var_scss)


css_files = get_css_files("css/themes")

themes = get_theme_list(css_files)
generate_include_all_mixins(themes)
generate_classes_for_all_themes(themes)

structure = generate_basic_structure(css_files)
generate_highlight_scss(structure)
generate_var_css(css_files, structure)
