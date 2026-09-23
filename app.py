import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

CORS(app)

# OpenAI API key environment variable se read hogi
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/")
def home():
    return "AI Email Reply Assistant Backend is Running!"


@app.route("/generate-reply", methods=["POST"])
def generate_reply():

    try:
        # Check request data
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        # Get email and tone
        email = data.get("email", "").strip()
        tone = data.get("tone", "Formal")

        # Check empty email
        if email == "":
            return jsonify({
                "error": "Please enter an email first."
            }), 400

        # AI prompt
        prompt = f"""
You are an AI Email Reply Assistant.

Write a professional email reply to the following email.

Tone: {tone}

Original email:
{email}

Rules:
- Keep the reply clear and natural.
- Do not add unnecessary information.
- Match the requested tone.
- Include a suitable greeting and closing.
"""

        # OpenAI API call
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        reply = response.output_text

        # Successful response
        return jsonify({
            "reply": reply
        }), 200

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": "Something went wrong while generating the reply. Please try again."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )