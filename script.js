const toggleTarget = document.getElementById('darkModeToggle');

function setDarkMode(isDark) {
  document.body.classList.toggle('dark-mode', isDark);
  localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
}

// On load
if (localStorage.getItem('darkMode') === 'enabled') {
  setDarkMode(true);
}

// On click
toggleTarget.addEventListener('click', () => {
  const isDark = !document.body.classList.contains('dark-mode');
  setDarkMode(isDark);
});

