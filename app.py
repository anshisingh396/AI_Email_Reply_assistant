import os

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


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

        # Demo replies
        if tone == "Formal":

            reply = f"""Dear Sir/Madam,

Thank you for your email.

I have received your message regarding the following matter:

{email}

I will review the details and get back to you accordingly.

Best regards,
AI Email Reply Assistant"""

        elif tone == "Friendly":

            reply = f"""Hi,

Thanks for reaching out!

I received your email regarding:

{email}

I’ll get back to you soon with the required information.

Best,
AI Email Reply Assistant"""

        else:  # Polite

            reply = f"""Dear Sir/Madam,

Thank you for contacting me.

I appreciate your email regarding:

{email}

I will look into the matter and respond as soon as possible.

Kind regards,
AI Email Reply Assistant"""

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
