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

    # VERIFY
    if request.method == "GET":

        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == VERIFY_TOKEN:
            return challenge, 200

        return "fail", 403


    # COMMENT EVENT
    if request.method == "POST":

        data = request.json

        print("DATA:",data)

        try:

            change = data["entry"][0]["changes"][0]["value"]

            comment_text = change.get("text","")
            comment_id = change.get("id")

            print("COMMENT:",comment_text)
            print("COMMENT ID:",comment_id)

            # TEST için her yoruma cevap
            response = requests.post(

                f"https://graph.facebook.com/v19.0/{comment_id}/replies",

                json={
                    "message":"Bot aktif 🚀",
                    "access_token":PAGE_TOKEN
                }

            )

            print("REPLY STATUS:",response.text)

        except Exception as e:

            print("ERROR:",e)

        return "ok"


if __name__ == "__main__":

    port = int(os.environ.get("PORT",8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
