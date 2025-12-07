from flask import Flask, request
import requests
import os
import joblib

app = Flask(__name__)

BOT_ID = "faee69f69254a556971bf5e8b0"

# Load the scam detection model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "TechyTerps", "model", "models", "naive_bayes_pipeline.pkl")
scam_model = None

def load_model():
    """Load the Naive Bayes scam detection model."""
    global scam_model
    try:
        if os.path.exists(MODEL_PATH):
            scam_model = joblib.load(MODEL_PATH)
            print(f"Scam detection model loaded successfully from {MODEL_PATH}")
        else:
            print(f"Warning: Model file not found at {MODEL_PATH}")
            print("Scam detection will be disabled until model is trained and exported.")
    except Exception as e:
        print(f"Error loading scam detection model: {e}")
        scam_model = None

def is_scam(text):
    """Check if a message is a scam using the trained model."""
    if scam_model is None:
        return False, 0.0
    try:
        prediction = scam_model.predict([text])[0]
        probabilities = scam_model.predict_proba([text])[0]
        confidence = max(probabilities)
        is_scam_msg = prediction == "Scam" or prediction == 1
        return is_scam_msg, confidence
    except Exception as e:
        print(f"Error during scam prediction: {e}")
        return False, 0.0

# Load model when module is imported
load_model()


@app.route("/", methods=["GET", "HEAD"])
def head_check():
    return "ok", 200


@app.route("/", methods=["POST"])
def callback():
    data = request.get_json()
    print("Received webhook:", data)
    if not data:
        return "ok", 200

    memberid = data.get("member_id", "")
    name = data.get("name", "")
    text = data.get("text", "")
    text_lower = text.lower()
    
    if not text:
        return "ok", 200

    # Check for scam messages first
    scam_detected, confidence = is_scam(text)
    if scam_detected and confidence > 0.7:
        warning_msg = f"Warning: This message from {name} may be a scam (confidence: {confidence:.1%}). Please be cautious and do not click any suspicious links or share personal information."
        send_message(warning_msg)
        print(f"Scam detected from {name}: {text[:50]}... (confidence: {confidence:.1%})")
        return "ok", 200

    # Normal bot responses
    if "hello" in text_lower:
        send_message("Hey there! I'm your bot running on Replit.")
    elif "ping" in text_lower:
        send_message("pong")
    elif "bye" in text_lower:
        send_message("See you later! " + name)

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

