# Python

```python
def available_next(itrbl):
    """
    Splits an iterable into two streams
    i is the normal ordered iterable
    n is the next element from i
    """
    i, n = tee(itrbl, 2)
    n = chain(islice(n, 1, None), [None])
    return zip(i, n)
```

## Javascript

```javascript
function switchTheme(e) {
  if (e.target.checked) {
    currentTheme = 'light';
  }
  else {
    currentTheme = 'dark';
  }
  document.documentElement.setAttribute('data-theme', currentTheme);
  localStorage.setItem('theme', currentTheme);
}
```

### SCSS

```scss
@mixin dark-scheme {
  --font-color: #e3e0d7;
  --bg-color: #242424;
  --heading-color: #fff;
  --link-color: #80a0ff;
  --link-color-visited: #d787ff;
}
@media (prefers-color-scheme: dark) {
  :root {
    @include dark-scheme;
  }
}
[data-theme="dark"]:root {
  @include dark-scheme;
}
```

### HTML

```html
<header>
  <nav class="theme-switch-wrapper">
    <h1>{{ page.title }}</h1>
    <label class="theme-switch" for="checkbox">
      <input type="checkbox" id="checkbox" />
      <div class="round slider"></div>
    </label>
  </nav>
</header>
```
