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

        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")

        return "fail"


    if request.method == "POST":

        try:

            data = request.get_json()

            print("DATA:",data)

            value = data["entry"][0]["changes"][0]["value"]

            comment_id = value["id"]

            print("COMMENT ID:",comment_id)

            reply_url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

            payload = {

                "message":"Bot aktif 🚀",
                "access_token":PAGE_TOKEN

            }

            response = requests.post(reply_url,data=payload)

            print("REPLY STATUS:",response.text)

        except Exception as e:

            print("ERROR:",e)

        return "ok"
