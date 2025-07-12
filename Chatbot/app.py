from flask import Flask, request, render_template, jsonify
import json
import random
import re

app = Flask(__name__)

with open("intents.json") as f:
    intents = json.load(f)

def get_response(user_input):
    user_input = user_input.lower()
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if re.search(pattern.lower(), user_input):
                return random.choice(intent["responses"])
    return "I'm not sure I understand. Can you rephrase?"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
