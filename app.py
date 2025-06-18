user_sessions = {
    'whatsapp:+2507xxxxxx': {
        'step': 'language_selection',  # or 'waiting_for_option', etc.
        'language': 'en'  # or 'rw'
    }
}
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Memory to track each user's session
user_sessions = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    response = MessagingResponse()
    msg = response.message()

    # Start session if user is new
    if sender not in user_sessions:
        user_sessions[sender] = {'step': 'language_selection'}
        msg.body("Muraho neza! / Hello! I’m Engineer Shyaka from Inzu.ai 👷🏾‍♂️.\n\nPlease choose your preferred language:\n1️⃣ Kinyarwanda\n2️⃣ English")
        return str(response)

    # Handle language selection
    if user_sessions[sender]['step'] == 'language_selection':
        if incoming_msg == '1':
            user_sessions[sender]['language'] = 'rw'
            user_sessions[sender]['step'] = 'menu'
            msg.body("Murakoze! Hitamo:\n1️⃣ Ohereza igishushanyo cy’inzu yawe\n2️⃣ Mfungurira uburyo bwo kugikora bushya")
        elif incoming_msg == '2':
            user_sessions[sender]['language'] = 'en'
            user_sessions[sender]['step'] = 'menu'
            msg.body("Thank you! Choose an option:\n1️⃣ Upload your existing floor plan\n2️⃣ Generate a new one with my help")
        else:
            msg.body("Please reply with:\n1️⃣ for Kinyarwanda\n2️⃣ for English")
        return str(response)

    # In the next step we’ll handle the menu options
    # ...

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Memory store to track user sessions
user_sessions = {}

@app.route("/")
def home():
    return "Construction bot is live!"

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    response = MessagingResponse()
    msg = response.message()

    # Check if sender is already in session
    user_data = user_sessions.get(sender, {})

    if 'language' not in user_data:
        # If greeting detected, start language selection
        if incoming_msg in ['hi', 'hello', 'muraho', 'bite', 'bonjour', 'salut']:
            msg.body("👷🏽 Hey welcome! I'm Engineer Shyaka from Inzu.ai.\n\n"
                     "👇 Which language would you like to use?\n1. English\n2. Kinyarwanda\n\n"
                     "Hit *1* or *2* to choose.")
        elif incoming_msg == '1':
            user_data['language'] = 'en'
            user_sessions[sender] = user_data
            msg.body("✅ Thank you! Now tell me — do you have a house floor plan already, or would you like us to help generate one?")
        elif incoming_msg == '2':
            user_data['language'] = 'rw'
            user_sessions[sender] = user_data
            msg.body("✅ Murakoze! Noneho tubwire niba ufite igishushanyo cy’inzu cyangwa wifuza ko tugufashe kugikora.")
        else:
            msg.body("👋 Welcome to Inzu.ai!\nPlease reply with *1* for English or *2* for Kinyarwanda to continue.")
    else:
        # Later steps will go here based on language and next logic
        lang = user_data['language']
        if lang == 'en':
            msg.body("🛠 Awesome! Next step coming soon...")
        else:
            msg.body("🛠 Ni byiza! Igikorwa gikurikira kiraje...")

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
