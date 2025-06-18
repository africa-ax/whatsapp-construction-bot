from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
user_sessions = {}

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    response = MessagingResponse()
    msg = response.message()

    # Initialize session
    user_data = user_sessions.get(sender, {})

    # Step 1: Language selection
    if 'language' not in user_data:
        if incoming_msg in ['hi', 'hello', 'muraho', 'bite', 'bonjour', 'salut']:
            msg.body("👷🏽 Hey welcome! I'm Engineer Shyaka from Inzu.ai.\n\n"
                     "👇 Which language would you like to use?\n1. English\n2. Kinyarwanda\n\n"
                     "Hit *1* or *2* to choose.")
            user_data['step'] = 'language_selection'
            user_sessions[sender] = user_data
            return str(response)

        elif incoming_msg == '1':
            user_data['language'] = 'en'
            user_data['step'] = 'main_menu'
            user_sessions[sender] = user_data
            msg.body("✅ Thank you! Now tell me — do you have a house floor plan already, or would you like us to help generate one?\n\n1️⃣ I have a floor plan\n2️⃣ Help me generate one")
            return str(response)

        elif incoming_msg == '2':
            user_data['language'] = 'rw'
            user_data['step'] = 'main_menu'
            user_sessions[sender] = user_data
            msg.body("✅ Murakoze! Noneho tubwire niba ufite igishushanyo cy’inzu cyangwa wifuza ko tugufashe kugikora.\n\n1️⃣ Mfite igishushanyo\n2️⃣ Mfungurira uburyo bwo kugikora bushya")
            return str(response)

        else:
            msg.body("👋 Welcome to Inzu.ai!\nPlease reply with *1* for English or *2* for Kinyarwanda to continue.")
            return str(response)

    # Step 2: Main menu
    elif user_data.get('step') == 'main_menu':
        lang = user_data.get("language")

        if incoming_msg == '1':
            user_data["step"] = "upload_plan"
            user_sessions[sender] = user_data
            msg.body("📤 Great! Please upload your house floor plan (image or PDF)." if lang == "en"
                     else "📤 Neza cyane! Twohereze igishushanyo cy’inzu yawe (ishusho cyangwa PDF).")

        elif incoming_msg == '2':
            user_data["step"] = "generate_plan"
            user_sessions[sender] = user_data
            msg.body("🧠 No problem! Let’s generate one. Please answer a few questions." if lang == "en"
                     else "🧠 Nta kibazo! Reka tugufashe kugikora. Subiza ibibazo bike.")

        else:
            msg.body("⚠️ Please reply with *1* or *2*." if lang == "en"
                     else "⚠️ Nyamuneka hitamo *1* cyangwa *2*.")
        return str(response)

    # Next steps placeholders
    elif user_data.get('step') == 'upload_plan':
        msg.body("📥 (Coming soon) We’ll process your uploaded plan." if user_data['language'] == "en"
                 else "📥 (Biraza) Tuzatangira gusesengura igishushanyo cyawe.")
        return str(response)

    elif user_data.get('step') == 'generate_plan':
        msg.body("📝 (Coming soon) We'll ask questions to generate your plan." if user_data['language'] == "en"
                 else "📝 (Biraza) Tuzagutangira kukubaza ibibazo kugira ngo tugufashe kugikora.")
        return str(response)

    else:
        msg.body("⚠️ Sorry, I didn’t understand that. Please say 'hi' to start again.")
        return str(response)

if __name__ == "__main__":
    app.run(debug=True)
