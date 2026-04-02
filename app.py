from flask import Flask, request
import requests
import os

app = Flask(__name__)

PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = "yapaycevapla123"


@app.route("/")
def home():
    return "Bot aktif"


@app.route("/webhook", methods=["GET","POST"])
def webhook():

    if request.method == "GET":

        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == VERIFY_TOKEN:
            return challenge

        return "fail"


    if request.method == "POST":

        data = request.json
        print(data)

        try:

            change = data["entry"][0]["changes"][0]["value"]

            comment_id = change["id"]

            print("COMMENT ID:",comment_id)

            url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

            payload = {
                "message":"Bot aktif 🚀",
                "access_token":PAGE_TOKEN
            }

            r = requests.post(url,data=payload)

            print("REPLY:",r.text)

        except Exception as e:

            print("ERROR:",e)

        return "ok"


port = int(os.environ.get("PORT",8080))

app.run(host="0.0.0.0",port=port)
