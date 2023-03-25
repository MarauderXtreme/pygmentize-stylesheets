# Pygments-Stylesheets

Jekyll and therefore Github Pages uses the rogue gem for code highlighting which itself is compatible with pygments stylesheets.
Unfortunately they are not readily available and there is no up-to-date archive of those stylesheets.
One can use the pygmentize programm to generate a simple css file.
This helps a bit but for advanced usages in web design this lacks some support.

Especially in the case of dark and light themes which can be switched by most modern browsers a more flexible way of interacting with those stylsheets is of benefit.
To keep the moving JS parts to a minimum one can interact with media-queries and CSS variables to be able to switch between dark and light themes easily.

Unfortunaly each theme comes with a unique set of CSS rules which makes it hard for a central crafted file.
As of writing this (beginning of 2023) there are 283 unique variables across 176 stylesheets.
Therefore an automated way to generate those files and variables is needed.

## Purpose

For one this repo should serve as an up-to-date archive of the normal pygments stylesheets.
Additionally it should provide generated drop-in files for more advanced use of those code highlighting themes.
All those generated files should be automatically updated and release either on package updates or on a schedule. (github-actions)

## Currently available stylesheets

- each of the builtin pygments themes (see [get_styles][get_styles])
- thirdparty packaged theme listed [from here][pipfile]

See for all theme names [css][css] or [themes][themes].

[get_styles]: src/get_styles.py
[pipfile]: Pipfile#L9
[css]: docs/css/themes
[themes]: docs/dist/themes/

## Preview the themes

Find information on how to use the various generated files and preview the themes here:
<https://marauderxtreme.github.io/pygmentize-stylesheets/>

## Include further thirdparty stylesheets

Pypi was extensively searched for unique packages that provide stylesheet.
If there are missing ones please check if they actually work with the scripts and send a PR.
There are currently not compatible thirdparty packages that have been excluded.

## Automatic archive updates

It is the intention that the archive of CSS and CSS variables files will be updated either on a schedule or after package updates.
If there is a useful way maybe even a npm package could be created.
TBD

## Future

Currently even though the generated CSS variable files are name `.scss` they are in fact simple CSS files.
Maybe it will be possible to generate nested SCSS for the central highlighting file.

## Excluded stylesheets

- `pygments-style-goggles` (depends on goggles and breaks everything)
- `pygments-style-soft-era` (has one broken CSS-rule)

## Is it any good

[Yes](https://news.ycombinator.com/item?id=3067434)
