user_sessions = {
    'whatsapp:+2507xxxxxx': {
        'step': 'language_selection',  # or 'waiting_for_option', etc.
        'language': 'en'  # or 'rw'
    }
}
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# User session memory
user_sessions = {}

@app.route("/")
def home():
    return "✅ Inzu.ai WhatsApp bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From", "")
    response = MessagingResponse()
    msg = response.message()

    # Initialize session if new
    if sender not in user_sessions:
        user_sessions[sender] = {"step": "language_selection"}
        msg.body(
            "👷🏽 Hey, welcome! I'm Engineer Shyaka from Inzu.ai.\n\n"
            "👇 Which language would you like to use?\n1️⃣ English\n2️⃣ Kinyarwanda\n\n"
            "Reply with *1* or *2* to continue."
        )
        return str(response)

    session = user_sessions[sender]

    # Handle language selection
    if session["step"] == "language_selection":
        if incoming_msg == "1":
            session["language"] = "en"
            session["step"] = "main_menu"
            msg.body(
                "✅ Thank you! Now tell me — do you have a house floor plan already, or would you like us to help generate one?\n"
                "1️⃣ I have a floor plan\n2️⃣ Help me generate one"
            )
        elif incoming_msg == "2":
            session["language"] = "rw"
            session["step"] = "main_menu"
            msg.body(
                "✅ Murakoze! Noneho tubwire niba ufite igishushanyo cy’inzu cyangwa wifuza ko tugufashe kugikora:\n"
                "1️⃣ Mfite igishushanyo\n2️⃣ Mfungurira uburyo bwo kugikora bushya"
            )
        else:
            msg.body("Please reply with *1* or *2* to select your language.")
        return str(response)

    # Placeholder for next steps
    if session["step"] == "main_menu":
        lang = session["language"]
        if lang == "en":
            msg.body("🛠 Awesome! Next step coming soon...")
        else:
            msg.body("🛠 Ni byiza! Igikorwa gikurikira kiraje...")

        return str(response)

    # Fallback
    msg.body("Sorry, I didn’t understand that. Please type *hi* to start.")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
