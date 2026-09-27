(function () {
    var bar = document.getElementById('page-loading-bar')
    var overlay = document.getElementById('page-loading-overlay')
    if (!bar || !overlay) return

    function startLoading() {
        bar.classList.remove('finish')
        void bar.offsetWidth
        bar.classList.add('active')
        overlay.classList.add('active')
    }

    function stopLoading() {
        bar.classList.remove('active')
        bar.classList.add('finish')
        setTimeout(function () { bar.classList.remove('finish') }, 300)
        overlay.classList.remove('active')
    }

    function isInternalLink(link) {
        if (!link || !link.href) return false
        if (link.target === '_blank') return false
        if (link.hasAttribute('download')) return false
        if (link.origin !== window.location.origin) return false
        if (link.getAttribute('href') && link.getAttribute('href').startsWith('#')) return false
        return true
    }

    document.addEventListener('click', function (e) {
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
        var link = e.target.closest('a')
        if (!isInternalLink(link)) return
        e.preventDefault()
        startLoading()
        document.body.classList.add('page-exit')
        setTimeout(function () {
            window.location.href = link.href
        }, 650)
    })

    document.addEventListener('submit', function (e) {
        var form = e.target
        if (form.dataset.noTransition) return
        e.preventDefault()

        if (e.submitter && e.submitter.name) {
            var hidden = document.createElement('input')
            hidden.type = 'hidden'
            hidden.name = e.submitter.name
            hidden.value = e.submitter.value
            form.appendChild(hidden)
        }

        if (e.submitter && e.submitter.classList.contains('quiz-btn')) {
            e.submitter.classList.add('quiz-btn-selected')
            var siblingButtons = form.querySelectorAll('.quiz-btn')
            siblingButtons.forEach(function (btn) {
                if (btn !== e.submitter) btn.classList.add('quiz-btn-dimmed')
            })
        }

        startLoading()
        document.body.classList.add('page-exit')
        setTimeout(function () {
            form.submit()
        }, 650)
    })

    window.addEventListener('pageshow', function () {
        stopLoading()
        document.body.classList.remove('page-exit')
    })
})()
