from flask import Flask, request
import os

app = Flask(__name__)

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
        else:
            return "fail"

    if request.method == "POST":

        data = request.json
        print("WEBHOOK GELDİ:", data)

        return "ok"

app.run(host="0.0.0.0",port=8080)
