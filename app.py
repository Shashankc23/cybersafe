import os

from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

questions = [
    {
        "email": "From: prizes@r0blox-free-robux.com\nSubject: You won FREE Robux!\n\nHi Player,\n\nCongratulations! You have been chosen to receive 10,000 FREE Robux!\nClick here RIGHT NOW to claim your prize before it expires:\nhttp://r0blox-free-robux.com/claim",
        "answer": "phishing",
        "explanation": "Great catch — that's phishing! Roblox's real website is roblox.com, but this one sneaks in a zero instead of the letter 'o': r0blox. Byte's tip: nobody just gives away free Robux to a random person. If a message sounds too good to be true, it probably is."
    },
    {
        "email": "From: no-reply@youtube.com\nSubject: Your YouTube comment got a reply\n\nHi there,\n\nSomeone replied to your comment on a video. Click below to see what they said:\nhttps://youtube.com/comments\n\nIf this wasn't you, you can ignore this email.",
        "answer": "legit",
        "explanation": "This one's the real deal. It's from youtube.com, it's calm instead of scary, and it even says you can ignore it if it wasn't you. Byte's tip: safe emails never pressure you — they just tell you what happened and let you decide."
    },
    {
        "email": "From: support@minecraf t-helpdesk.net\nSubject: Your Minecraft account will be DELETED!\n\nDear Player,\n\nWe found something wrong with your account. You have 1 hour to log in or your account will be gone FOREVER.\nFix it now: http://minecraf t-free.net/save-account",
        "answer": "phishing",
        "explanation": "This is a scam. Minecraft's real website is minecraft.net, not 'minecraf t-helpdesk.net' with that weird extra space. Byte's tip: the 1-hour countdown is meant to scare you into not thinking it through. Real companies never rush you like that."
    },
    {
        "email": "From: donotreply@spotify.com\nSubject: Your Spotify Family invite is ready\n\nHi,\n\nYou have been invited to join a Spotify Family plan. To accept, just open the Spotify app or visit spotify.com.\n\nIf you were not expecting this, you can ignore this email.",
        "answer": "legit",
        "explanation": "This one's safe. It comes from spotify.com, doesn't ask for any personal information, and tells you to just use the real app if you want to accept. Byte's tip: real invites send you to the actual app, not a strange link."
    },
    {
        "email": "From: kidssupport@disney-prize-winner.com\nSubject: You won a trip to Disneyland!\n\nHi Lucky Winner,\n\nYou have been randomly selected to win a FREE family trip to Disneyland!\nTo claim your prize, send us your full name, home address, and parent's phone number:\nhttp://disney-prize-winner.com/claim-now",
        "answer": "phishing",
        "explanation": "Definitely fake. Disney's real site is disney.com, not 'disney-prize-winner.com'. Byte's tip: this email wants your home address and your parent's phone number — that's exactly the kind of information a scammer needs to cause real trouble. Never send that to claim a prize."
    },
    {
        "email": "From: security@paypa1-support.com\nSubject: Unusual sign-in detected\n\nDear Customer,\n\nWe detected a sign-in from a new device. If this wasn't you, verify your account immediately by entering your login details here:\nhttp://paypa1-support.com/verify",
        "answer": "phishing",
        "explanation": "Sharp eyes needed here — it's 'paypa1' with the number 1 instead of the letter 'l'. Byte's tip: real companies never ask you to 'verify' your account by typing your password into a link from an email. If you're ever unsure, open the app yourself instead of clicking the link."
    },
    {
        "email": "From: noreply@nintendo.com\nSubject: Your Switch Online membership is expiring soon\n\nHi,\n\nYour Nintendo Switch Online membership will expire in 7 days. You can renew anytime from the Nintendo eShop on your console. No action is needed if you don't wish to renew.\n\nThanks,\nNintendo",
        "answer": "legit",
        "explanation": "This is a normal, safe email. It's calm, doesn't push a suspicious link, and points you to renew through the actual console — not a website. Byte's tip: real account emails usually tell you to go handle things in the app or device you already trust."
    },
    {
        "email": "From: giveaway@fortnite-vbucks-gift.com\nSubject: You've been selected for 13,500 FREE V-Bucks!\n\nHey Gamer,\n\nOur system randomly selected your account for a FREE V-Bucks reward! Click below and enter your Epic Games username and password to receive your gift before it's given to someone else:\nhttp://fortnite-vbucks-gift.com/claim",
        "answer": "phishing",
        "explanation": "Classic V-Bucks scam. Fortnite doesn't run random giveaways like this, and no real company ever needs both your username AND password to give you something free. Byte's tip: this exact trick has fooled thousands of kids — now you know better."
    },
]

password_questions = [
    {
        "password": "password123",
        "answer": "weak",
        "explanation": "Nope, this one's weak. 'password123' is the most guessed password on the planet — hackers try it first, every single time. Byte's tip: never use the actual word 'password' anywhere in your password!"
    },
    {
        "password": "Tr0ub4dor&3!",
        "answer": "strong",
        "explanation": "Now that's a strong one! It mixes capital and lowercase letters, swaps letters for numbers, and throws in a symbol. Byte's tip: that mix is exactly what makes a password hard to guess, even for a computer trying millions of combinations."
    },
    {
        "password": "minecraft2014",
        "answer": "weak",
        "explanation": "This one's weak. Your favorite game plus a year — often your birth year — is easy for someone who knows you to guess. Byte's tip: hackers also have lists of popular game names they try automatically."
    },
    {
        "password": "MyD0g$N@medMax!",
        "answer": "strong",
        "explanation": "Strong! It's a phrase you could actually remember, but with capital letters, number swaps, and symbols mixed in. Byte's tip: that's the sweet spot — strong enough to stump a hacker, simple enough for you to recall."
    },
    {
        "password": "123456",
        "answer": "weak",
        "explanation": "Way too weak. '123456' is the single most common password in the world, and it takes a hacker's computer less than a second to crack it. Byte's tip: always mix letters, numbers, and symbols together."
    },
    {
        "password": "qwerty",
        "answer": "weak",
        "explanation": "Weak — 'qwerty' is just the top row of the keyboard. Byte's tip: hackers know every keyboard pattern trick, so patterns like this get cracked just as fast as '123456'."
    },
    {
        "password": "Purple7$Kite!Jumps",
        "answer": "strong",
        "explanation": "Strong! It's a long string of unrelated words mixed with a capital, a number, and symbols, so it doesn't spell out anything personal about you. Byte's tip: the longer and more random it looks, the longer it takes a computer to crack."
    },
    {
        "password": "ilovemymom",
        "answer": "weak",
        "explanation": "This one's weak, even though it's sweet. It's all lowercase letters with no numbers or symbols. Byte's tip: length alone isn't enough — you still need that mix of capitals, numbers, and symbols to make it strong."
    },
]

browsing_questions = [
    {
        "scenario": "A website pops up saying: \"CONGRATULATIONS! You are today's lucky visitor! Click here to claim your FREE iPhone 15!\"\nThe website address is: http://free-prizes-4u.net/claim",
        "answer": "sketchy",
        "explanation": "Sketchy for sure. Nobody picks random visitors to win free iPhones — that's just not how prizes work. Byte's tip: this site also uses HTTP instead of HTTPS and has no padlock, and 'free-prizes-4u.net' has nothing to do with Apple. Close the tab."
    },
    {
        "scenario": "You search for a free Minecraft mod. The top result is from a site called 'minecraftmods.org'. You click it and it immediately starts downloading a file called 'MinecraftMod_FREE_installer.exe' without you clicking anything.",
        "answer": "sketchy",
        "explanation": "Big red flag. Safe websites never download files to your computer without you clicking a button first. Byte's tip: an automatic download like this could easily be malware — close the tab, don't open the file, and tell a trusted adult."
    },
    {
        "scenario": "While watching a YouTube video, a big red pop-up fills your screen: \"VIRUS DETECTED! Your computer is infected with 3 viruses! Call 0800-FIX-NOW immediately or your files will be deleted!\"",
        "answer": "sketchy",
        "explanation": "This is a fake virus warning — one of the oldest tricks on the internet. Byte's tip: real antivirus software never shows a pop-up telling you to call a phone number. Just press Escape or close the tab. Never call the number."
    },
    {
        "scenario": "You search for 'Roblox' and click the first result. The page looks exactly like Roblox, but the address bar shows: http://roblox-play-now.info/home",
        "answer": "sketchy",
        "explanation": "Sketchy. The real Roblox website is roblox.com, not 'roblox-play-now.info'. Byte's tip: scammers are really good at copying the look of a website, but they can't copy the actual web address — always check that part."
    },
    {
        "scenario": "You visit your school's homework portal. The address bar shows: https://homework.myschool.edu and there is a little padlock icon next to the address.",
        "answer": "safe",
        "explanation": "This one's safe. The padlock means the site locks up your information like a locked diary, so no one else can peek at it on the way there. Byte's tip: a real school address (.edu) plus the padlock is a great sign you're in the right place."
    },
    {
        "scenario": "A pop-up appears while you're browsing: \"Your battery is critically low! Install this Battery Booster app now to fix it!\"",
        "answer": "sketchy",
        "explanation": "Fake alert. Websites can't actually check your device's battery — that information isn't something a webpage can see. Byte's tip: this trick just wants you to install an app that could actually harm your device. Close it and move on."
    },
    {
        "scenario": "You click a link a friend sent in a game chat. It goes to steamcommunity-gifts.net offering a free skin if you log in with your game account.",
        "answer": "sketchy",
        "explanation": "Sketchy. The real Steam Community site is steamcommunity.com, not a lookalike domain with extra words tacked on. Byte's tip: fake gift sites like this exist for one reason — to steal your login. Even if a friend sent it, they might have been tricked too."
    },
    {
        "scenario": "You want to look up a homework answer, so you visit your teacher's official class website that your teacher gave you the link to in class.",
        "answer": "safe",
        "explanation": "This one's safe. A website address given directly by a trusted adult, like your teacher, is one of the safest ways to find a site — you know exactly where it came from. Byte's tip: that's very different from clicking a random link from a search result or a stranger."
    },
]

privacy_questions = [
    {
        "scenario": "You just made a new friend in an online game. They seem really nice and ask: \"What school do you go to? I want to see if we live near each other!\"",
        "answer": "unsafe",
        "explanation": "This one's unsafe. Even a friendly-seeming online friend is still someone you don't really know. Byte's tip: your school name tells a stranger exactly where to find you every single school day — only share that with people you know in real life."
    },
    {
        "scenario": "Your mom is ordering something online and steps away from the laptop. You can see her card number on the screen. Your friend asks what you are doing and you describe what is on the screen.",
        "answer": "unsafe",
        "explanation": "Unsafe. A card number belongs to your parents, not you, and sharing it — even with a friend just chatting — could lead to someone spending money that isn't theirs. Byte's tip: if you ever see card details on a screen, that's a 'keep it to yourself' moment."
    },
    {
        "scenario": "You take a cool photo in your backyard and want to post it online. Before posting, you turn off the location setting on your phone so the photo does not include where it was taken.",
        "answer": "safe",
        "explanation": "Great thinking, that's safe! Photos can secretly store your exact location inside the file. Byte's tip: turning off location before you even take the photo means strangers can never use your picture to find out where you live."
    },
    {
        "scenario": "A website is running a contest to win a game console. To enter, it asks for your full name, home address, and phone number. The site looks fun and the prize looks real.",
        "answer": "unsafe",
        "explanation": "Unsafe. Contests that ask for your home address and phone number are a very common trick to collect personal information. Byte's tip: even if the prize seems real, never fill out a form like this without a trusted adult checking it first."
    },
    {
        "scenario": "Someone in a group chat you are in asks everyone to share their phone number so the group can move to a different app. You don't recognize all the people in the chat.",
        "answer": "unsafe",
        "explanation": "Unsafe. Your phone number is personal information, and sharing it in a group where you don't know everyone means strangers could contact you directly. Byte's tip: tell a trusted adult about requests like this."
    },
    {
        "scenario": "You're setting up a new gaming profile and choose a username that doesn't include your real name, age, or school.",
        "answer": "safe",
        "explanation": "Nice work, that's safe! Byte's tip: a username with zero personal details makes it much harder for a stranger to figure out who you actually are or where to find you."
    },
    {
        "scenario": "An app you downloaded asks for permission to see your exact location at all times, even when you're not using the app.",
        "answer": "unsafe",
        "explanation": "Unsafe. Most apps don't actually need to track your location 24/7 just to work. Byte's tip: always check with a trusted adult before letting any app have constant access to where you are."
    },
    {
        "scenario": "You get a message from an unknown number asking to video chat because they 'just want to see your face.'",
        "answer": "unsafe",
        "explanation": "Unsafe. You don't owe a stranger a video chat, ever. Byte's tip: requests like this from someone you don't know in real life should always be reported to a trusted adult right away."
    },
]

social_engineering_questions = [
    {
        "scenario": "A player you met yesterday online says, 'I work for the game company. Your account might be deleted unless you tell me your username and password so I can check it.'",
        "answer": "dont_trust",
        "explanation": "Don't trust this one. This person is pretending to have authority to scare you into handing over information. Byte's tip: real game companies never ask for your password through a chat message — not ever."
    },
    {
        "scenario": "Someone sends you a message saying, 'Your best friend told me your birthday, but I forgot it. Can you tell me again?'",
        "answer": "dont_trust",
        "explanation": "Don't trust this. Mentioning your friend is meant to make the request feel harmless. Byte's tip: personal details like your birthday shouldn't be handed over just because a message name-drops someone you know — check with that friend directly first."
    },
    {
        "scenario": "A person in a game says, 'I'll tell everyone you're mean if you don't send me a screenshot of your profile page.'",
        "answer": "dont_trust",
        "explanation": "Don't trust this — that's manipulation through threats. Byte's tip: if someone tries to pressure or threaten you into sharing information or images, don't do it, and tell a trusted adult right away."
    },
    {
        "scenario": "Someone online says, 'I bet you're too scared to prove you're really 12. Send me a picture of your school ID if you're telling the truth.'",
        "answer": "dont_trust",
        "explanation": "Don't trust this. It's a dare designed to make you feel like you have something to prove. Byte's tip: school IDs have personal information on them and should never be sent to someone online, no matter the dare."
    },
    {
        "scenario": "A classmate asks if you want to join a school club meeting after class and tells you when and where it is.",
        "answer": "trust",
        "explanation": "This one's fine to trust! It's a normal, everyday conversation — no personal info being requested, no pressure, no tricks. Byte's tip: this is what a safe, ordinary message from someone you know actually looks like."
    },
    {
        "scenario": "A stranger online says, 'I'm actually a talent scout for a big YouTube channel. Send me your parent's email and phone number so we can set up a meeting.'",
        "answer": "dont_trust",
        "explanation": "Don't trust this. Real opportunities go through official channels, not a random message suddenly asking for your parents' contact info. Byte's tip: this is a classic setup just to collect personal information."
    },
    {
        "scenario": "Someone says, 'Everyone in the clan already voted you out unless you send $20 in gift cards by tonight.'",
        "answer": "dont_trust",
        "explanation": "Don't trust this. It combines a deadline with a request for money — two huge red flags at once. Byte's tip: no real group or team would ever demand a payment like this to stay in."
    },
    {
        "scenario": "A new online friend says, 'I trust you, so I'll tell you a secret if you tell me one back — like your parents' Wi-Fi password.'",
        "answer": "dont_trust",
        "explanation": "Don't trust this. It's a manipulation trick called 'reciprocity' — making you feel like you owe them something personal in return. Byte's tip: never trade real information like a password, even for a 'secret.'"
    },
]

footprint_questions = [
    {
        "scenario": "You want to post a funny video of your friend online, but you haven't asked them if it's okay yet.",
        "answer": "unsafe",
        "explanation": "Unsafe — always ask first. It's their moment too, and once something is online, it can be shared, screenshotted, and saved by anyone. Byte's tip: even if you take it down later, you can't take back the copies other people already made."
    },
    {
        "scenario": "Before posting a photo from your school project, you double check that no street signs or house numbers are visible in the background.",
        "answer": "safe",
        "explanation": "Nice catch, that's safe! Checking the whole background — not just the middle of the photo — for clues about where you live is a genuinely smart habit. Byte's tip: keep doing this every time before you post."
    },
    {
        "scenario": "You post an embarrassing photo, then delete it five minutes later. But by then, two friends already took screenshots of it.",
        "answer": "unsafe",
        "explanation": "Unsafe. Deleting a post doesn't delete the copies other people already made. Byte's tip: think before you post, not after — once it's out there, you can't fully take it back."
    },
    {
        "scenario": "You're about to type your full name and age into a public profile on a gaming forum.",
        "answer": "unsafe",
        "explanation": "Unsafe. Public profiles can be seen by total strangers, not just people you know. Byte's tip: keep your full name, age, and other personal details off of any public page."
    },
    {
        "scenario": "Before posting a video, you show it to a parent first to make sure it's okay to share.",
        "answer": "safe",
        "explanation": "Safe, and a great habit! Getting a trusted adult's opinion before posting means someone else can spot things you might miss. Byte's tip: a second pair of eyes catches a lot."
    },
    {
        "scenario": "You tag your exact location on a photo posted publicly right when you take it at the park near your house.",
        "answer": "unsafe",
        "explanation": "Unsafe. A live location tag on a public post can show anyone exactly where you are right now, close to home. Byte's tip: turn off live location tagging, especially on anything public."
    },
    {
        "scenario": "You're proud of a school award and want to post about it. You share the news without including your school's name or your full name.",
        "answer": "safe",
        "explanation": "Safe, and go ahead and celebrate! Byte's tip: leaving out identifying details like your school name lets you share good news without giving away where to find you."
    },
    {
        "scenario": "You make a private account so only approved friends can see your posts, and you only accept requests from people you know in real life.",
        "answer": "safe",
        "explanation": "Safe — this is one of the strongest habits you can build. Byte's tip: a private account with real-life friends only means strangers can't even see your digital footprint in the first place."
    },
]

cyberbullying_questions = [
    {
        "scenario": "Someone keeps leaving mean comments on your posts, so you block them and tell a parent.",
        "answer": "good",
        "explanation": "Good move! Blocking and telling a trusted adult is exactly the right call. Byte's tip: you never have to deal with a bully all by yourself."
    },
    {
        "scenario": "A group chat starts making fun of a classmate. You leave the chat and tell a trusted adult what happened.",
        "answer": "good",
        "explanation": "Good move! Walking away and speaking up helps stop bullying instead of letting it continue. Byte's tip: that takes real courage, and it's exactly the right thing to do."
    },
    {
        "scenario": "Someone keeps sending you insulting messages in a game, so you send back even meaner messages to make them stop.",
        "answer": "bad",
        "explanation": "Bad move. Fighting back usually makes things worse and can turn into a bigger fight. Byte's tip: block the person and tell a trusted adult instead of trying to out-mean them."
    },
    {
        "scenario": "You see a classmate getting made fun of in a group chat, so you join in because everyone else is doing it.",
        "answer": "bad",
        "explanation": "Bad move. Joining in still hurts the other person, even if you didn't start it. Byte's tip: it's always okay to just not participate — and telling an adult helps even more."
    },
    {
        "scenario": "A mean comment upsets you, so instead of replying, you take a screenshot and show it to a parent.",
        "answer": "good",
        "explanation": "Good move! Screenshotting proof and telling a trusted adult is smart. Byte's tip: it gives them exactly what they need to actually help you."
    },
    {
        "scenario": "You notice a friend hasn't been talking much lately. You ask them privately if everything is okay after seeing some mean comments on their page.",
        "answer": "good",
        "explanation": "Good move! Checking in privately on a friend who might be struggling is a kind, upstander thing to do. Byte's tip: a small check-in can mean a lot to someone going through a hard time."
    },
    {
        "scenario": "Someone spreads a rumor about you online, so you make a fake account to spread rumors back about them.",
        "answer": "bad",
        "explanation": "Bad move. Retaliating, even by spreading rumors back, makes you part of the problem and can get you in trouble too. Byte's tip: report it to a trusted adult instead of trying to get even."
    },
    {
        "scenario": "You get a hurtful message and immediately reply with a long paragraph defending yourself and insulting them back.",
        "answer": "bad",
        "explanation": "Bad move. Arguing back, even to defend yourself, usually escalates things further. Byte's tip: save the message, block the person, and go straight to a trusted adult instead of typing a reply."
    },
]

gaming_questions = [
    {
        "scenario": "A player in your favorite game offers to trade you a super rare skin if you send them your account login 'just to verify you're a real player.'",
        "answer": "sketchy",
        "explanation": "Sketchy. Byte's tip: no legitimate trade ever requires your login. This is one of the most common ways gaming accounts get stolen — never share your password, even for a 'rare' item."
    },
    {
        "scenario": "You want to buy in-game currency, so you use the official in-game store instead of a random website offering the same currency for way cheaper.",
        "answer": "safe",
        "explanation": "Safe move! Byte's tip: third-party sites selling in-game currency for cheap are almost always scams that steal payment info or accounts — the official store is always the safer bet."
    },
    {
        "scenario": "Someone you just met in a voice chat asks you to download a 'special aim-assist tool' from a link they send you.",
        "answer": "sketchy",
        "explanation": "Sketchy. Byte's tip: 'special tools' from strangers are a classic way to sneak malware onto your device. Only download game mods or tools from the official site or trusted, well-known sources."
    },
    {
        "scenario": "A random teammate says they'll report you and get you banned unless you send them your rare items right now.",
        "answer": "sketchy",
        "explanation": "Sketchy — that's a threat used to scare you into handing over items. Byte's tip: random players can't actually get you banned like that. Don't send anything, and report their message instead."
    },
    {
        "scenario": "Before accepting a friend request in a game, you check that you actually recognize the person from real life or a trusted group.",
        "answer": "safe",
        "explanation": "Safe habit! Byte's tip: not every friend request needs to be accepted. Being selective about who can message or add you cuts down on scam attempts a lot."
    },
    {
        "scenario": "A pop-up inside a mobile game says you won a free gift card — just enter your email and phone number to claim it.",
        "answer": "sketchy",
        "explanation": "Sketchy. Byte's tip: in-game 'you won!' pop-ups asking for personal info are almost always ads in disguise trying to collect your data, not real prizes."
    },
    {
        "scenario": "You mute and report a player who keeps sending you inappropriate messages during a match, instead of replying to them.",
        "answer": "safe",
        "explanation": "Safe and smart! Byte's tip: mute and report is exactly the right response — it protects you without escalating things, and it flags the behavior to the game's moderators."
    },
    {
        "scenario": "A stream sniper offers to boost your rank in a competitive game if you share your account password with them for the weekend.",
        "answer": "sketchy",
        "explanation": "Sketchy. Byte's tip: sharing your password with anyone — even someone offering to 'help' — means they can lock you out, spend your money, or get your account banned. Never share account logins."
    },
]

twofactor_questions = [
    {
        "scenario": "When setting up a new game account, you turn on two-factor authentication (2FA) so a code from your phone is needed to log in, not just a password.",
        "answer": "good",
        "explanation": "Good move! Byte's tip: 2FA means that even if someone steals your password, they still can't get into your account without your phone too. It's one of the single best protections you can turn on."
    },
    {
        "scenario": "A message claims to be from a game company saying your 2FA code expired and asks you to read your current code out loud over voice chat to 'renew' it.",
        "answer": "bad",
        "explanation": "Bad — that's a scam. Byte's tip: a 2FA code is never something you share with anyone, ever, including someone claiming to work for the company. Real companies never ask for it directly."
    },
    {
        "scenario": "You set up 2FA using an authenticator app on your phone instead of just text messages, since text messages can sometimes be intercepted.",
        "answer": "good",
        "explanation": "Good move! Byte's tip: an authenticator app generates codes directly on your device, which is generally considered more secure than codes sent by text message."
    },
    {
        "scenario": "You get a 2FA code text you didn't request, so you enter it into the site anyway just to see what happens.",
        "answer": "bad",
        "explanation": "Bad move. Byte's tip: an unexpected 2FA code usually means someone else already has your password and is trying to log in. Never enter a code you didn't request — change your password instead."
    },
    {
        "scenario": "You write down your backup 2FA codes and keep them somewhere safe at home instead of just screenshotting them on your phone.",
        "answer": "good",
        "explanation": "Good move! Byte's tip: backup codes let you get back into your account if you lose your phone. Keeping a physical copy somewhere safe is smarter than a screenshot that could be seen if your phone is lost."
    },
    {
        "scenario": "You decide 2FA is annoying and turn it off on your gaming account because typing in a code every time feels like a hassle.",
        "answer": "bad",
        "explanation": "Bad move. Byte's tip: that extra code is exactly what stops someone else from getting into your account with just a stolen password. A few extra seconds is worth the protection."
    },
    {
        "scenario": "You set up 2FA on your email account, since your email can be used to reset passwords for almost all of your other accounts.",
        "answer": "good",
        "explanation": "Good move, and a smart priority! Byte's tip: your email is often the master key to your other accounts, so protecting it with 2FA protects everything connected to it too."
    },
    {
        "scenario": "A friend asks you to send them the 2FA code that just popped up on your phone so they can log into 'their' account that's apparently linked to your number.",
        "answer": "bad",
        "explanation": "Bad move. Byte's tip: a 2FA code that lands on your phone is meant to protect your account. Sharing it with anyone, even a friend, defeats the entire purpose of having it."
    },
]

MODULES = {
    'phishing': {
        'questions': questions,
        'lesson_template': 'phishing_lesson.html',
        'quiz_template': 'phishing.html',
        'lesson_url': '/phishing',
        'quiz_url': '/phishing/quiz',
        'check_url': '/check',
        'complete_url': '/complete',
        'next_url': '/passwords',
    },
    'password': {
        'questions': password_questions,
        'lesson_template': 'passwords_lesson.html',
        'quiz_template': 'passwords.html',
        'lesson_url': '/passwords',
        'quiz_url': '/passwords/quiz',
        'check_url': '/check_password',
        'complete_url': '/complete_password',
        'next_url': '/browsing',
    },
    'browsing': {
        'questions': browsing_questions,
        'lesson_template': 'browsing_lesson.html',
        'quiz_template': 'browsing.html',
        'lesson_url': '/browsing',
        'quiz_url': '/browsing/quiz',
        'check_url': '/check_browsing',
        'complete_url': '/complete_browsing',
        'next_url': '/privacy',
    },
    'privacy': {
        'questions': privacy_questions,
        'lesson_template': 'privacy_lesson.html',
        'quiz_template': 'privacy.html',
        'lesson_url': '/privacy',
        'quiz_url': '/privacy/quiz',
        'check_url': '/check_privacy',
        'complete_url': '/complete_privacy',
        'next_url': '/social',
    },
    'social': {
        'questions': social_engineering_questions,
        'lesson_template': 'social_lesson.html',
        'quiz_template': 'social.html',
        'lesson_url': '/social',
        'quiz_url': '/social/quiz',
        'check_url': '/check_social',
        'complete_url': '/complete_social',
        'next_url': '/footprint',
    },
    'footprint': {
        'questions': footprint_questions,
        'lesson_template': 'footprint_lesson.html',
        'quiz_template': 'footprint.html',
        'lesson_url': '/footprint',
        'quiz_url': '/footprint/quiz',
        'check_url': '/check_footprint',
        'complete_url': '/complete_footprint',
        'next_url': '/bullying',
    },
    'bullying': {
        'questions': cyberbullying_questions,
        'lesson_template': 'bullying_lesson.html',
        'quiz_template': 'bullying.html',
        'lesson_url': '/bullying',
        'quiz_url': '/bullying/quiz',
        'check_url': '/check_bullying',
        'complete_url': '/complete_bullying',
        'next_url': '/gaming',
    },
    'gaming': {
        'questions': gaming_questions,
        'lesson_template': 'gaming_lesson.html',
        'quiz_template': 'gaming.html',
        'lesson_url': '/gaming',
        'quiz_url': '/gaming/quiz',
        'check_url': '/check_gaming',
        'complete_url': '/complete_gaming',
        'next_url': '/twofactor',
    },
    'twofactor': {
        'questions': twofactor_questions,
        'lesson_template': 'twofactor_lesson.html',
        'quiz_template': 'twofactor.html',
        'lesson_url': '/twofactor',
        'quiz_url': '/twofactor/quiz',
        'check_url': '/check_twofactor',
        'complete_url': '/complete_twofactor',
        'next_url': '/',
    },
}


def make_lesson_view(config):
    def view():
        return render_template(config['lesson_template'])
    return view


def make_quiz_view(name, config):
    def view():
        index = session.get(f'{name}_index', 0)
        question = config['questions'][index]
        return render_template(
            config['quiz_template'],
            question=question,
            score=session.get(f'{name}_score', 0),
            question_number=index + 1,
            total_questions=len(config['questions']),
        )
    return view


def make_check_view(name, config):
    def view():
        questions_list = config['questions']
        index = session.get(f'{name}_index', 0)
        question = questions_list[index]
        if request.form['answer'] == question['answer']:
            result = 'Correct'
            session[f'{name}_score'] = session.get(f'{name}_score', 0) + 10
            session[f'{name}_streak'] = session.get(f'{name}_streak', 0) + 1
        else:
            result = 'Wrong'
            session[f'{name}_streak'] = 0

        streak = session[f'{name}_streak']

        next_index = index + 1
        is_last = next_index == len(questions_list)
        if is_last:
            session[f'{name}_final_score'] = session.get(f'{name}_score', 0)
            session[f'{name}_index'] = 0
            session[f'{name}_score'] = 0
            session[f'{name}_streak'] = 0
        else:
            session[f'{name}_index'] = next_index

        score = session.get(f'{name}_final_score' if is_last else f'{name}_score', 0)
        return render_template(
            'result.html',
            result=result,
            explanation=question['explanation'],
            score=score,
            streak=streak,
            is_last=is_last,
            complete_url=config['complete_url'],
            continue_url=config['quiz_url'],
        )
    return view


def make_complete_view(name, config):
    def view():
        score = session.get(f'{name}_final_score', 0)
        return render_template(
            'complete.html',
            score=score,
            retry_url=config['quiz_url'],
            next_url=config['next_url'],
            module=name,
        )
    return view


for module_name, module_config in MODULES.items():
    app.add_url_rule(module_config['lesson_url'], f'{module_name}_lesson', make_lesson_view(module_config))
    app.add_url_rule(module_config['quiz_url'], f'{module_name}_quiz', make_quiz_view(module_name, module_config))
    app.add_url_rule(module_config['check_url'], f'{module_name}_check', make_check_view(module_name, module_config), methods=['POST'])
    app.add_url_rule(module_config['complete_url'], f'{module_name}_complete', make_complete_view(module_name, module_config))


@app.route('/pet')
def pet():
    return render_template('pet.html')


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
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
