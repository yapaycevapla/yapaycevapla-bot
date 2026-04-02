from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "yapaycevapla123"

@app.route("/", methods=["GET"])
def home():
    return "Bot aktif"

@app.route("/webhook", methods=["GET","POST"])
def webhook():

    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        return "fail", 403

    if request.method == "POST":
        data = request.get_json()

        print("WEBHOOK GELDİ:")
        print(data)

        return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT",8080))
    app.run(host="0.0.0.0", port=port)
