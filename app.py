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

            value = data["entry"][0]["changes"][0]["value"]

            comment = value.get("text","")
            comment_id = value.get("id")

            print("COMMENT:",comment)

            # mention yoksa cevap verme
            if "@yapaycevapla" not in comment.lower():
                return "ok"

            # BOT CEVABI
            requests.post(

                f"https://graph.facebook.com/v25.0/{comment_id}/replies",

                params={

                    "message":"Merhaba 👋 YapayCevapla bot aktif.",
                    "access_token":PAGE_TOKEN

                }

            )

        except Exception as e:

            print("ERROR:",e)

        return "ok"


if __name__ == "__main__":

    port = int(os.environ.get("PORT",8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
