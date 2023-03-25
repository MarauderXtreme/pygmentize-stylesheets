---
nav-index: 0
---

# Overview

Welcome to an updated pygments stylesheet archive with added value for use with the rogue highlighter and henceforth Jekyll.

## How To Use

With the option for CSS and SCSS-mixins there are many ways to include the pygments stylesheets

### CSS

If just a theme is needed with no SCSS just look for the desired theme and download the corresponding CSS.
The file needs to be placed in the sites assets and be included in the `<head>`.

```html
<head>
  <title>My awesome site</title>
  <link href="/assets/css/pygments-theme.css" rel="stylesheet" type="text/css">
</head>
```

Configure `Jekyll` to use `rogue` as the code highlighter.
This should come now by default and no extra options should be necesary but here is an example for the `_config.yml`.

```yml
markdown: kramdown
kramdown:
  syntax_highlighter: rouge
```

There is also the possibility to include the files directly from this site but be careful since everything can change and break without notice.
Just subsitute `THEMENAME` with the desired theme.

```html
<head>
  <title>My awesome site</title>
  <link href="{{ site.url }}{{ site.baseurl }}/docs/css/themes/THEMENAME.css" rel="stylesheet" type="text/css">
</head>
```

### SCSS

The css theme can also be included within SCSS.
Look for the desired theme and download it into the assets and import it into the appropriate SCSS file.

```scss
@charset "utf-8";
@import 'THEMENAME';
```

### SCSS with `@mixin`

If a bit more flexibility but still only one theme is needed download the `highlight.scss` into the assets and import it in the SCSS.
Afterwards download the desired theme scss into the assets and include it as well.
Use the provided theme `@mixin` on a top-level object or where needed.

```scss
@charset "utf-8";
@import 'highlight';
@import 'THEMENAME';

:root {
  @include THEMENAME-pygment;
}
```

### Dark and light theme with SCSS

A switching theme based on the visitors settings can be achieved with the use of media queries.
Download the `highlight.scss` into the assets and import it in the SCSS.
Afterwards download a theme for dark and one for light into the assets and include them aswell.
Use the provided `@mixin` on a top-level but wrap it with the media query `prefers-color-scheme` for dark and for light.

```scss
@charset "utf-8";
@import 'highlight';
@import 'THEMENAME-dark';
@import 'THEMENAME-light';

@media (prefers-color-scheme: dark) {
  :root {
    @include THEMENAME-dark-pygment;
  }
}
@media (prefers-color-scheme: light) {
  :root {
    @include THEMENAME-light-pygment;
  }
}
```

Give it a try on this site.
If javascript is enabled a theme switcher can be found in the top right corner.

{% include themes.html %}
