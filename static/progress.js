const PROGRESS_KEY = 'cybersafe_progress'
const MAX_SCORE_PER_MODULE = 50
const MODULE_ORDER = ['phishing', 'password', 'browsing', 'privacy', 'social', 'footprint', 'bullying', 'gaming', 'twofactor']

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
    localStorage.removeItem(PET_NAME_KEY)
}

const PET_STAGES = [
    { minXP: 0, name: 'Hatchling Byte', scale: 0.75, glow: 'none', blurb: "Byte just hatched! Answer questions correctly to help Byte grow." },
    { minXP: 75, name: 'Byte Jr.', scale: 0.87, glow: 'none', blurb: "Byte is growing! Keep learning to help Byte level up more." },
    { minXP: 150, name: 'Byte', scale: 1, glow: '0 0 20px rgba(0,87,255,.25)', blurb: "Byte is officially online and glowing with knowledge." },
    { minXP: 225, name: 'Super Byte', scale: 1.08, glow: '0 0 30px rgba(0,87,255,.4)', blurb: "Super Byte! You two make a great cybersecurity team." },
    { minXP: 300, name: 'Mega Byte', scale: 1.16, glow: '0 0 40px rgba(93,44,255,.5)', blurb: "Mega Byte! Almost nothing can trick you two now." },
    { minXP: 375, name: 'Max Byte', scale: 1.25, glow: '0 0 55px rgba(255,193,7,.6)', blurb: "Max Byte, fully powered up! You've mastered every module." },
]

function getPetStage(xp) {
    let stage = PET_STAGES[0]
    for (const s of PET_STAGES) {
        if (xp >= s.minXP) stage = s
    }
    return stage
}

const PET_NAME_KEY = 'cybersafe_pet_name'

function getPetName() {
    return localStorage.getItem(PET_NAME_KEY) || 'Byte'
}

function setPetName(name) {
    const trimmed = (name || '').trim().slice(0, 20)
    if (trimmed) localStorage.setItem(PET_NAME_KEY, trimmed)
}

const MODULE_META = {
    phishing: { label: 'Phishing Defense', icon: '🪝' },
    password: { label: 'Password Strength', icon: '🔐' },
    browsing: { label: 'Safe Browsing', icon: '🌐' },
    privacy: { label: 'Privacy Awareness', icon: '👁️' },
    social: { label: 'Social Engineering', icon: '🎭' },
    footprint: { label: 'Digital Footprint', icon: '👣' },
    bullying: { label: 'Cyberbullying Response', icon: '🛡️' },
    gaming: { label: 'Gaming Safety', icon: '🎮' },
    twofactor: { label: 'Two-Factor Authentication', icon: '🔑' },
}
