# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Simple in-memory user sessions
user_sessions = {}

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Construction Bot is running"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    from_number = request.values.get("From", "")
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Start a new session if none exists
    if from_number not in user_sessions:
        user_sessions[from_number] = {
            "step": "intro",
            "plot_size": None,
            "bedrooms": None
        }

    session = user_sessions[from_number]

    # MAIN CHAT LOGIC
    if incoming_msg == "restart":
        session["step"] = "intro"
        session["plot_size"] = None
        session["bedrooms"] = None
        msg.body("Session restarted. What is your plot size? (e.g., 10x20 meters)")
    
    elif session["step"] == "intro":
        msg.body("👋 Hi! I’m your Construction Bot.\nLet’s design your house.\nWhat is your plot size? (e.g., 10x20 meters)")
        session["step"] = "ask_plot_size"

    elif session["step"] == "ask_plot_size":
        session["plot_size"] = incoming_msg
        msg.body("✅ Got it! Now, how many bedrooms do you want?")
        session["step"] = "ask_bedrooms"

    elif session["step"] == "ask_bedrooms":
        session["bedrooms"] = incoming_msg
        msg.body("✅ Thanks! Generating your floor plan and cost estimate... (coming soon)")
        session["step"] = "done"

    elif session["step"] == "done":
        msg.body("🎉 You're done! Type 'restart' to begin again.")

    else:
        msg.body("❓ I didn’t understand that. Type 'restart' to begin again.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
