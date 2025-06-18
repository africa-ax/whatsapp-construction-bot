user_sessions = {
    'whatsapp:+2507xxxxxx': {
        'step': 'language_selection',  # or 'waiting_for_option', etc.
        'language': 'en'  # or 'rw'
    }
}
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Store sessions per user (by phone number)
user_sessions = {}

@app.route("/")
def home():
    return "🚧 Inzu.ai Construction Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    response = MessagingResponse()
    msg = response.message()

    # Get or initialize session
    session = user_sessions.get(sender, {"step": "greeting"})
    
    # Step 1: Greet and ask for language
    if session["step"] == "greeting":
        if incoming_msg in ['hi', 'hello', 'muraho', 'bite', 'bonjour', 'salut']:
            session["step"] = "language_selection"
            user_sessions[sender] = session
            msg.body("👷🏽 Hey, welcome! I'm Engineer Shyaka from Inzu.ai.\n\n"
                     "👇 Which language would you like to use?\n1️⃣ English\n2️⃣ Kinyarwanda\n\n"
                     "Reply with *1* or *2* to continue.")
            return str(response)
        
        elif incoming_msg == '1':
            session["language"] = "en"
            session["step"] = "main_menu"
            user_sessions[sender] = session
            msg.body("✅ Thank you! Now tell me — do you have a house floor plan already, or would you like us to help generate one?\n"
                     "1️⃣ I have a floor plan\n2️⃣ Help me generate one")
            return str(response)

        elif incoming_msg == '2':
            session["language"] = "rw"
            session["step"] = "main_menu"
            user_sessions[sender] = session
            msg.body("✅ Murakoze! Noneho tubwire niba ufite igishushanyo cy’inzu cyangwa wifuza ko tugufashe kugikora:\n"
                     "1️⃣ Mfite igishushanyo\n2️⃣ Mfungurira uburyo bwo kugikora bushya")
            return str(response)

        else:
            msg.body("👋 Welcome to Inzu.ai!\nPlease reply with:\n1️⃣ for English\n2️⃣ for Kinyarwanda")
            return str(response)

    # Step 2: Main menu based on chosen language
    elif session["step"] == "main_menu":
        lang = session.get("language", "en")
        if lang == "en":
            msg.body("🛠 Great! Next step will be implemented soon. Stay tuned.")
        else:
            msg.body("🛠 Ni byiza! Igikorwa gikurikira kiraza vuba. Tegereza gato.")

        return str(response)

    # Default fallback
    msg.body("Sorry, I didn’t understand that. Please say 'hi' to start.")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
