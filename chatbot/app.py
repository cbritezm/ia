import random
import queries
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def generate_reply(user_text: str) -> str:
    """Very small canned-response engine.

    Swap this out for a real model/API call (OpenAI, Anthropic, a local
    model, etc.) whenever you're ready to wire up an actual assistant.
    """
    text = user_text.lower().strip()
    response = ""

    if text.startswith(("hi", "hey", "hello", "hola")):
        response = "Hola. Como puedo ayudarte hoy?"
    if "help" in text or "ayuda" in text:
        response = "Dime un poco mas detalladamente lo que necesitas y hare mi maximo esfuerzo para ayudarte"
    if "thank" in text or "gracias" in text:
        response =  "Cuando gustes."
    if "?" in text and len(text) == 1:
        response =  "Buena pregunta. Quizas necesitemos algo mas de informacion para ayudarte"

    fallback = [
        "Got it. Tell me more.",
        "Interesting — go on.",
        "Noted. Anything else?",
        "I hear you. What's the next step?",
    ]

    if len(response) == 0:
        response = queries.query_response(text)

    if len(response) == 0:
        response = "No dispongo informacion de este topico"
    return response


@app.route("/")
def index():
    return render_template("index.html")




@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_text = (data.get("message") or "").strip()

    if not user_text:
        return jsonify({"error": "Message cannot be empty."}), 400

    reply = generate_reply(user_text)
    return jsonify({"reply": reply})


if __name__ == "__main__":
#    app.run(debug=True)
    app.run(host="127.0.0.1", port=5000)

