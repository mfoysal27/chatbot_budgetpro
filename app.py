from flask import Flask, request
import requests
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = "my_verify_token"

@app.route("/webhook", methods=["GET"])
def verify():
    # Facebook sends a GET request to verify the webhook
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification token mismatch", 403

@app.route("/webhook", methods=["POST"])
def handle_message():
    data = request.get_json()
    if "message" in data["entry"][0]["messaging"][0]:
        sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
        message = data["entry"][0]["messaging"][0]["message"]["text"]
        reply(sender_id, f"You said: {message}")
    return "ok", 200

def reply(recipient_id, text):
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={EAASbpkAZAi6cBP0pUZAU3f0aWBVy23EvcdEsuBZChF40kp5CwyVvNZBPfbudEgLL5D1ZCo2ZAwO1ybjUeSQZBMLrK5IMqauG5VUGDc2RZBCLJ0xomXnqqP2T3E3TMkoRpmY3Lf3CFv58xUBq0DMaZAi0iJaNbAPylEtgnpKxC0WzMalHXIgHZABMisH69IoiefZCDZC1rINNV7X5KwZDZD}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
