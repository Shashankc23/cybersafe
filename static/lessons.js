function initLessonSlides(rootId) {
    const root = document.getElementById(rootId)
    if (!root) return
    const slides = Array.from(root.querySelectorAll('.lesson-slide'))
    const dotsWrap = root.querySelector('.lesson-dots')
    let current = 0

    slides.forEach(function () {
        if (dotsWrap) {
            const dot = document.createElement('span')
            dot.className = 'lesson-dot'
            dotsWrap.appendChild(dot)
        }
    })
    const dots = dotsWrap ? Array.from(dotsWrap.children) : []

    const prevBtn = root.querySelector('.lesson-prev')
    const nextBtn = root.querySelector('.lesson-next')
    const startBtn = root.querySelector('.lesson-start')
    const counter = root.querySelector('.lesson-counter')

    function show(i) {
        slides.forEach(function (slide, idx) {
            slide.style.display = idx === i ? 'block' : 'none'
        })
        dots.forEach(function (dot, idx) {
            dot.classList.toggle('active', idx === i)
        })
        if (prevBtn) prevBtn.style.visibility = i === 0 ? 'hidden' : 'visible'
        if (nextBtn) nextBtn.style.display = i === slides.length - 1 ? 'none' : 'inline-block'
        if (startBtn) startBtn.style.display = i === slides.length - 1 ? 'inline-block' : 'none'
        if (counter) counter.textContent = (i + 1) + ' / ' + slides.length
        current = i
        root.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { show(Math.max(0, current - 1)) })
    if (nextBtn) nextBtn.addEventListener('click', function () { show(Math.min(slides.length - 1, current + 1)) })

    show(0)
}
