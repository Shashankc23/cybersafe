function toggleTheme() {
    let theme = localStorage.getItem("theme")
    if (theme === "dark") {
        theme = "light"
    } else {
        theme = "dark"
    }
    localStorage.setItem("theme", theme)
    document.body.className = theme
    document.getElementById("theme-toggle").textContent = theme === "dark" ? "☀️" : "🌙"
}

window.onload = function() {
    let theme = localStorage.getItem("theme")
    document.body.className = theme
    document.getElementById("theme-toggle").textContent = theme === "dark" ? "☀️" : "🌙"
}
