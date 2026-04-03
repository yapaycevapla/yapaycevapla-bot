from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
print("TOKEN:", PAGE_TOKEN)

@app.route("/")
def home():
    return "bot aktif"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "fail"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    print("DATA:",data)

    try:

        change = data["entry"][0]["changes"][0]["value"]

        comment_id = change["id"]

        print("COMMENT ID:",comment_id)

        url = f"https://graph.facebook.com/v19.0/{comment_id}/replies?message=Bot aktif 🚀&access_token={PAGE_TOKEN}"

        r = requests.post(url)

        print("REPLY STATUS:",r.text)

    except Exception as e:

        print("ERROR:",e)

    return "ok"
