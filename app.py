from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Construction bot is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # You can add Green API logic here later
    return jsonify({"reply": "Thank you for contacting the Construction Bot!"})

if __name__ == '__main__':
    app.run()
  
