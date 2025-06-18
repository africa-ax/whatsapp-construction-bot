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
