import os
from flask import Flask, request, jsonify
from transformers import pipeline
from config import LLM
from chatbot.chatbot import process_message

app = Flask(__name__)

# Initialize global variables
chat_history = []
context = ""
grievance_stage = 0

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history, context, grievance_stage

    user_input = request.json.get('message')
    prompt = request.json.get('prompt', '')

    response_text, grievance_stage, context = process_message(user_input, chat_history, context, grievance_stage, LLM, prompt)
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "bot", "content": response_text})

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)