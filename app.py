from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# In-memory session storage
user_sessions = {}

@app.route("/", methods=["GET"])
def home():
    return "🏗️ Inzu.ai bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From", "")
    response = MessagingResponse()
    msg = response.message()

    # Get or create user session
    session = user_sessions.get(sender, {"step": "language_selection"})

    # Always start with language selection if not set
    if session.get("step") == "language_selection":
        if incoming_msg in ['hi', 'hello', 'muraho', 'bite', 'bonjour', 'salut']:
            msg.body(
                "👷🏾 Muraho neza! / Hello! I’m Engineer Shyaka from Inzu.ai 👷🏾\n\n"
                "👇 Please choose your language:\n"
                "1️⃣ Kinyarwanda\n"
                "2️⃣ English"
            )
        elif incoming_msg == "1":
            session["language"] = "rw"
            session["step"] = "next_step"
            msg.body("✅ Murakoze! Turakomeza mu Kinyarwanda...")
        elif incoming_msg == "2":
            session["language"] = "en"
            session["step"] = "next_step"
            msg.body("✅ Thank you! We'll continue in English...")
        else:
            msg.body(
                "👇 Please choose your language:\n"
                "1️⃣ Kinyarwanda\n"
                "2️⃣ English"
            )

        # Save session
        user_sessions[sender] = session
        return str(response)

    # Placeholder for next logic
    msg.body("🛠️ Next step coming soon...")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True
