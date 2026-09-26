const PROGRESS_KEY = 'cybersafe_progress'
const MAX_SCORE_PER_MODULE = 50
const MODULE_ORDER = ['phishing', 'password', 'browsing', 'privacy', 'social']

function getProgress() {
    try {
        return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || {}
    } catch (e) {
        return {}
    }
}

function saveModuleResult(moduleKey, score) {
    const progress = getProgress()
    const best = progress[moduleKey] || 0
    progress[moduleKey] = Math.max(best, score)
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress))
}

function getTotalXP() {
    const progress = getProgress()
    return Object.values(progress).reduce((sum, s) => sum + s, 0)
}

function getMaxXP() {
    return MODULE_ORDER.length * MAX_SCORE_PER_MODULE
}

function getCompletedCount() {
    return Object.keys(getProgress()).length
}

function resetProgress() {
    localStorage.removeItem(PROGRESS_KEY)
}
