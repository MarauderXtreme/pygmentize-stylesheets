const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
const matchMediaPrefLight = window.matchMedia('(prefers-color-scheme: light)');
var currentTheme = localStorage.getItem('theme');

if (currentTheme) {
	document.documentElement.setAttribute('data-theme', currentTheme);

	if (currentTheme === 'light' || matchMediaPrefLight.matches) {
		toggleSwitch.checked = true;
	}
}

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

function onSystemThemeChange(e) {
	if (currentTheme) {
		return;
	}
	if (e.matches) {
		toggleSwitch.checked = true;
	}
	else {
		toggleSwitch.checked = false;
	}
}

toggleSwitch.addEventListener('change', switchTheme, false);
matchMediaPrefLight.addEventListener('change', onSystemThemeChange)
