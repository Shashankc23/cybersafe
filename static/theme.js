function applyTheme(theme) {
    document.documentElement.classList.remove('light', 'dark')
    document.documentElement.classList.add(theme)
    const toggle = document.getElementById('theme-toggle')
    if (toggle) toggle.textContent = theme === 'dark' ? '☀️' : '🌙'
}

function toggleTheme() {
    const current = localStorage.getItem('theme') || 'light'
    const next = current === 'dark' ? 'light' : 'dark'
    localStorage.setItem('theme', next)
    applyTheme(next)
}

window.onload = function () {
    applyTheme(localStorage.getItem('theme') || 'light')
}
