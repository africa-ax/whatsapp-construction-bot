@app.route("/whatsapp", methods=["POST"])
# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    # BASIC HANDLING
    if "floor" in incoming_msg:
        msg.body("Great! I can help with that. What is your plot size in meters (e.g., 10x20)?")
    elif "estimate" in incoming_msg:
        msg.body("Sure! How many rooms or floors do you want to estimate for?")
    else:
        msg.body("Hi! I'm your Construction Bot 🤖\n\nReply with:\n- 'floor' to get a floor plan\n- 'estimate' for building cost.")
    
    return str(resp)

if __name__ == "__main__":
    app.run()
