from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = 'cybersafe123'

questions = [
    {
        "email": "From: prizes@r0blox-free-robux.com\nSubject: You won FREE Robux!\n\nHi Player,\n\nCongratulations! You have been chosen to receive 10,000 FREE Robux!\nClick here RIGHT NOW to claim your prize before it expires:\nhttp://r0blox-free-robux.com/claim",
        "answer": "phishing",
        "explanation": "Roblox's real website is roblox.com — notice the fake one uses a zero instead of the letter 'o': r0blox. Also, nobody just gives away free Robux! If something sounds too good to be true, it probably is."
    },
    {
        "email": "From: no-reply@youtube.com\nSubject: Your YouTube comment got a reply\n\nHi there,\n\nSomeone replied to your comment on a video. Click below to see what they said:\nhttps://youtube.com/comments\n\nIf this wasn't you, you can ignore this email.",
        "answer": "legit",
        "explanation": "This email is from youtube.com — the real YouTube website. It is calm, not scary, and just tells you about a reply. It also says you can ignore it if it wasn't you. That is what safe emails look like."
    },
    {
        "email": "From: support@minecraf t-helpdesk.net\nSubject: Your Minecraft account will be DELETED!\n\nDear Player,\n\nWe found something wrong with your account. You have 1 hour to log in or your account will be gone FOREVER.\nFix it now: http://minecraf t-free.net/save-account",
        "answer": "phishing",
        "explanation": "Minecraft's real website is minecraft.net — not 'minecraf t-helpdesk.net'. The email is also trying to scare you with a 1-hour countdown. Real companies do not threaten to delete your account like that."
    },
    {
        "email": "From: donotreply@spotify.com\nSubject: Your Spotify Family invite is ready\n\nHi,\n\nYou have been invited to join a Spotify Family plan. To accept, just open the Spotify app or visit spotify.com.\n\nIf you were not expecting this, you can ignore this email.",
        "answer": "legit",
        "explanation": "This email comes from spotify.com — the real Spotify. It does not ask you to click a dodgy link or give away any personal information. It even tells you to ignore it if it was a mistake. Safe and friendly!"
    },
    {
        "email": "From: kidssupport@disney-prize-winner.com\nSubject: You won a trip to Disneyland!\n\nHi Lucky Winner,\n\nYou have been randomly selected to win a FREE family trip to Disneyland!\nTo claim your prize, send us your full name, home address, and parent's phone number:\nhttp://disney-prize-winner.com/claim-now",
        "answer": "phishing",
        "explanation": "Disney's real website is disney.com — not 'disney-prize-winner.com'. This email is asking for your home address and phone number, which is very dangerous to give to strangers. Never share personal information like this!"
    },
]

password_questions = [
    {
        "password": "password123",
        "answer": "weak",
        "explanation": "'password123' is the most guessed password in the world. Hackers try it first every single time. Never use the word 'password' in your password!"
    },
    {
        "password": "Tr0ub4dor&3!",
        "answer": "strong",
        "explanation": "This looks random, mixes uppercase and lowercase letters, swaps letters for numbers, and has a symbol. That makes it incredibly hard to guess — even for a computer."
    },
    {
        "password": "minecraft2014",
        "answer": "weak",
        "explanation": "Using your favourite game plus a year (often your birth year!) is very easy for someone who knows you to guess. Hackers also try popular game names automatically."
    },
    {
        "password": "MyD0g$N@medMax!",
        "answer": "strong",
        "explanation": "A short phrase you can remember, with capital letters, number swaps, and symbols mixed in, makes a password that is both strong AND memorable. This is the sweet spot!"
    },
    {
        "password": "123456",
        "answer": "weak",
        "explanation": "'123456' is the single most common password on the planet. It takes a hacker less than one second to crack it. Always use a mix of letters, numbers, and symbols."
    },
]

browsing_questions = [
    {
        "scenario": "A website pops up saying: \"CONGRATULATIONS! You are today's lucky visitor! Click here to claim your FREE iPhone 15!\"\nThe website address is: http://free-prizes-4u.net/claim",
        "answer": "sketchy",
        "explanation": "Nobody picks random visitors to win free iPhones! This is a fake prize trick to get you to click a dodgy link. The website uses HTTP (not HTTPS), has no padlock, and the address 'free-prizes-4u.net' has nothing to do with Apple. Close the tab straight away."
    },
    {
        "scenario": "You search for a free Minecraft mod. The top result is from a site called 'minecraftmods.org'. You click it and it immediately starts downloading a file called 'MinecraftMod_FREE_installer.exe' without you clicking anything.",
        "answer": "sketchy",
        "explanation": "Safe websites NEVER download files to your computer without you clicking a button first. An automatic download is a massive red flag — that file could be malware. Close the tab, do NOT open the file, and tell a trusted adult."
    },
    {
        "scenario": "While watching a YouTube video, a big red pop-up fills your screen: \"VIRUS DETECTED! Your computer is infected with 3 viruses! Call 0800-FIX-NOW immediately or your files will be deleted!\"",
        "answer": "sketchy",
        "explanation": "This is a fake virus warning — one of the oldest tricks on the internet. Real antivirus software does NOT show pop-ups asking you to call a phone number. These scams try to scare you into calling. Press ESC or close the browser tab. Do NOT call the number."
    },
    {
        "scenario": "You search for 'BBC News' and click the first result. The page looks exactly like BBC News, but the address bar shows: http://bbc-news-today.info/home",
        "answer": "sketchy",
        "explanation": "The real BBC website is bbc.co.uk or bbc.com — not 'bbc-news-today.info'. Scammers copy the look of real websites to trick you. Always check the address bar matches the real website name before reading or clicking anything."
    },
    {
        "scenario": "You visit your school's homework portal. The address bar shows: https://homework.myschool.edu and there is a padlock icon next to the address.",
        "answer": "safe",
        "explanation": "HTTPS means the connection is encrypted — your data is protected on its way to the website. The padlock icon confirms this. A real school domain (.edu) with HTTPS and a padlock is a good sign you are in the right place."
    },
]

privacy_questions = [
    {
        "scenario": "You just made a new friend in an online game. They seem really nice and ask: \"What school do you go to? I want to see if we live near each other!\"",
        "answer": "unsafe",
        "explanation": "Even if someone seems friendly online, you do not actually know who they are. Sharing your school name tells a stranger exactly where to find you every single day. Only share your school name with people you know and trust in real life."
    },
    {
        "scenario": "Your mom is ordering something online and steps away from the laptop. You can see her card number on the screen. Your friend asks what you are doing and you describe what is on the screen.",
        "answer": "unsafe",
        "explanation": "A card number is private financial information — it belongs to your parents, not you. Sharing it, even with a friend, can lead to someone spending money that is not theirs. If you ever see card details on a screen, keep it to yourself."
    },
    {
        "scenario": "You take a cool photo in your garden and want to post it online. Before posting, you turn off the location setting on your phone so the photo does not include where it was taken.",
        "answer": "safe",
        "explanation": "Great thinking! Photos can secretly store your exact location inside them. Turning off location before taking a photo means strangers cannot use your picture to find out where you live. Always check this before posting photos online."
    },
    {
        "scenario": "A website is running a competition to win a games console. To enter, it asks for your full name, home address, and phone number. The site looks fun and the prize looks real.",
        "answer": "unsafe",
        "explanation": "Competitions that ask for your home address and phone number are a common trick to collect personal information. Even if the prize is real, you should never fill in a form like this without a parent checking it first. Show a trusted adult before entering anything online."
    },
    {
        "scenario": "Someone in a group chat you are in asks everyone to share their phone number so the group can move to a different app. You do not recognise all the people in the chat.",
        "answer": "unsafe",
        "explanation": "Your phone number is personal information. Sharing it in a group where you do not know everyone means strangers could contact you directly. Tell a trusted adult about the request and only share your number with people you know in real life."
    },
]

social_engineering_questions = [
    {
        "scenario": "A player you met yesterday online says, 'I work for the game company. Your account might be deleted unless you tell me your username and password so I can check it.'",
        "answer": "dont_trust",
        "explanation": "This person is pretending to have authority to scare you into giving away information. Real game companies do not ask for your password through chat messages."
    },
    {
        "scenario": "Someone sends you a message saying, 'Your best friend told me your birthday, but I forgot it. Can you tell me again?'",
        "answer": "dont_trust",
        "explanation": "The person is trying to make their request sound harmless by mentioning your friend. Personal details like your birthday should not be shared with people you do not know."
    },
    {
        "scenario": "A person in a game says, 'I'll tell everyone you're mean if you don't send me a screenshot of your profile page.'",
        "answer": "dont_trust",
        "explanation": "This is manipulation through threats and pressure. If someone tries to force you into sharing information or images, do not do it and tell a trusted adult."
    },
    {
        "scenario": "Someone online says, 'I bet you're too scared to prove you're really 12. Send me a picture of your school ID if you're telling the truth.'",
        "answer": "dont_trust",
        "explanation": "This person is challenging you to make you feel like you have to prove something. School IDs contain personal information and should never be shared with strangers."
    },
    {
        "scenario": "A classmate asks if you want to join a school club meeting after class and tells you when and where it is.",
        "answer": "trust",
        "explanation": "This is a normal, everyday conversation. The classmate is not asking for personal information, using pressure, or trying to trick you into doing something unsafe."
    },
]




@app.route('/phishing')
def phishing_lesson():
    return render_template('phishing_lesson.html')

@app.route('/phishing/quiz') #When someone visits phishing page, run function below
def phishing():
    index = session.get('phishing_index', 0)
    question = questions[index]
    return render_template('phishing.html', question=question, score=session.get('phishing_score', 0), question_number=index+1, total_questions=len(questions))

@app.route('/check', methods=['POST'])
def check():
    index = session.get('phishing_index', 0)
    question = questions[index]
    if request.form['answer'] == question['answer']:
        result = 'Correct'
        score = session.get('phishing_score', 0)
        score = score + 10
        session['phishing_score'] = score
    else:
        result = 'Wrong'
    next_index = index + 1
    is_last = next_index == len(questions)
    if is_last:
        session['phishing_final_score'] = session.get('phishing_score', 0)
        session['phishing_index'] = 0
        session['phishing_score'] = 0
    else:
        session['phishing_index'] = next_index
    return render_template('result.html', result=result, explanation=question['explanation'], score=session.get('phishing_final_score' if is_last else 'phishing_score', 0), is_last=is_last, complete_url='/complete', continue_url='/phishing/quiz')


@app.route('/complete')
def complete():
    score = session.get('phishing_final_score', 0)
    return render_template('complete.html', score=score, retry_url='/phishing/quiz', next_url='/passwords')

@app.route('/passwords')
def passwords_lesson():
    return render_template('passwords_lesson.html')

@app.route('/passwords/quiz')
def passwords():
    index = session.get('password_index', 0)
    question = password_questions[index]
    return render_template('passwords.html', question=question, score=session.get('password_score', 0), question_number=index+1, total_questions=len(password_questions))

@app.route('/check_password', methods=['POST'])
def check_password():
    index = session.get('password_index', 0)
    question = password_questions[index]
    if request.form['answer'] == question['answer']:
        result = 'Correct'
        score = session.get('password_score', 0)
        score = score + 10
        session['password_score'] = score
    else:
        result = 'Wrong'
    next_index = index + 1
    is_last = next_index == len(password_questions)
    if is_last:
        session['password_final_score'] = session.get('password_score', 0)
        session['password_index'] = 0
        session['password_score'] = 0
    else:
        session['password_index'] = next_index
    return render_template('result.html', result=result, explanation=question['explanation'], score=session.get('password_final_score' if is_last else 'password_score', 0), is_last=is_last, complete_url='/complete_password', continue_url='/passwords/quiz')

@app.route('/complete_password')
def complete_password():
    score = session.get('password_final_score', 0)
    return render_template('complete.html', score=score, retry_url='/passwords/quiz', next_url='/browsing')

@app.route('/browsing')
def browsing_lesson():
    return render_template('browsing_lesson.html')

@app.route('/browsing/quiz')
def browsing():
    index = session.get('browsing_index', 0)
    question = browsing_questions[index]
    return render_template('browsing.html', question=question, score=session.get('browsing_score', 0), question_number=index+1, total_questions=len(browsing_questions))

@app.route('/check_browsing', methods=['POST'])
def check_browsing():
    index = session.get('browsing_index', 0)
    question = browsing_questions[index]
    if request.form['answer'] == question['answer']:
        result = 'Correct'
        score = session.get('browsing_score', 0)
        score = score + 10
        session['browsing_score'] = score
    else:
        result = 'Wrong'
    next_index = index + 1
    is_last = next_index == len(browsing_questions)
    if is_last:
        session['browsing_final_score'] = session.get('browsing_score', 0)
        session['browsing_index'] = 0
        session['browsing_score'] = 0
    else:
        session['browsing_index'] = next_index
    return render_template('result.html', result=result, explanation=question['explanation'], score=session.get('browsing_final_score' if is_last else 'browsing_score', 0), is_last=is_last, complete_url='/complete_browsing', continue_url='/browsing/quiz')

@app.route('/complete_browsing')
def complete_browsing():
    score = session.get('browsing_final_score', 0)
    return render_template('complete.html', score=score, retry_url='/browsing/quiz', next_url='/privacy')


@app.route('/privacy')
def privacy_lesson():
    return render_template('privacy_lesson.html')

@app.route('/privacy/quiz')
def privacy():
    index = session.get('privacy_index', 0)
    question = privacy_questions[index]
    return render_template('privacy.html', question=question, score=session.get('privacy_score', 0), question_number=index+1, total_questions=len(privacy_questions))

@app.route('/check_privacy', methods=['POST'])
def check_privacy():
    index = session.get('privacy_index', 0)
    question = privacy_questions[index]
    if request.form['answer'] == question['answer']:
        result = 'Correct'
        score = session.get('privacy_score', 0)
        score = score + 10
        session['privacy_score'] = score
    else:
        result = 'Wrong'
    next_index = index + 1
    is_last = next_index == len(privacy_questions)
    if is_last:
        session['privacy_final_score'] = session.get('privacy_score', 0)
        session['privacy_index'] = 0
        session['privacy_score'] = 0
    else:
        session['privacy_index'] = next_index
    return render_template('result.html', result=result, explanation=question['explanation'], score=session.get('privacy_final_score' if is_last else 'privacy_score', 0), is_last=is_last, complete_url='/complete_privacy', continue_url='/privacy/quiz')

@app.route('/complete_privacy')
def complete_privacy():
    score = session.get('privacy_final_score', 0)
    return render_template('complete.html', score=score, retry_url='/privacy/quiz', next_url='/social')

@app.route('/social')
def social_lesson():
    return render_template('social_lesson.html')

@app.route('/social/quiz')
def social():
    index = session.get('social_index', 0)
    question = social_engineering_questions[index]
    return render_template('social.html', question=question, score=session.get('social_score', 0), question_number=index+1, total_questions=len(social_engineering_questions))

@app.route('/check_social', methods=['POST'])
def check_social():
    index = session.get('social_index', 0)
    question = social_engineering_questions[index]
    if request.form['answer'] == question['answer']:
        result = 'Correct'
        score = session.get('social_score', 0)
        score = score + 10
        session['social_score'] = score
    else:
        result = 'Wrong'
    next_index = index + 1
    is_last = next_index == len(social_engineering_questions)
    if is_last:
        session['social_final_score'] = session.get('social_score', 0)
        session['social_index'] = 0
        session['social_score'] = 0
    else:
        session['social_index'] = next_index
    return render_template('result.html', result=result, explanation=question['explanation'], score=session.get('social_final_score' if is_last else 'social_score', 0), is_last=is_last, complete_url='/complete_social', continue_url='/social/quiz')

@app.route('/complete_social')
def complete_social():
    score = session.get('social_final_score', 0)
    return render_template('complete.html', score=score, retry_url='/social/quiz', next_url='/')


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/modules')
def modules():
    return render_template('modules.html')


if __name__ == '__main__':
    app.run(debug=True)



