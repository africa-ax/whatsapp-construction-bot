from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def home():
    return "Construction bot is live!"

@app.route("/webhook", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hello" in incoming_msg or "hi" in incoming_msg:
        msg.body("👋 Hello! I’m your Construction Cost Bot. Send me the dimensions of your house to get started.")
    elif "3 bedroom" in incoming_msg:
        msg.body("🧱 For a 3-bedroom house, estimated cost is about 25 million RWF. Want a floor plan or 3D view?")
    elif "floor plan" in incoming_msg:
        msg.body("📐 Floor plan generation is coming soon! Stay tuned.")
    else:
        msg.body("🤖 Sorry, I didn’t understand that. Try typing something like: ‘3 bedroom’ or ‘floor plan’.")

    return str(resp)

if __name__ == "__main__":
    app.run()
