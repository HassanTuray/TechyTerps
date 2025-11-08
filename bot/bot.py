from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_ID = "8ecefd266b2c66ba43b5d936de"


@app.route("/", methods=["GET", "HEAD"])
def head_check():
    return "ok", 200


@app.route("/", methods=["POST"])
def callback():
    data = request.get_json()
    print("Received webhook:", data)
    if not data:
        return "ok", 200

    text = data.get("text", "").lower()
    if not text:
        return "ok", 200

    if "hello" in text:
        send_message("Hey there! I'm your bot running on Replit.")
    elif "ping" in text:
        send_message("pong")
    elif "bye" in text:
        send_message("Goodbye!")

    return "ok", 200


def send_message(msg):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {"bot_id": BOT_ID, "text": msg}
    try:
        r = requests.post(url, json=payload)
        print("Sent message:", msg, "status:", r.status_code)
    except Exception as e:
        print("Error sending message:", e)


if __name__ == "__main__":
    print("Bot server starting on Replit...")
    app.run(host="0.0.0.0", port=8080)
