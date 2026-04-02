from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route("/")
def home():
    return "bot aktif"

@app.route("/webhook", methods=["GET","POST"])
def webhook():

    if request.method == "GET":
        if request.args.get("hub.verify_token") == "yapaycevapla123":
            return request.args.get("hub.challenge")
        return "fail"

    if request.method == "POST":

        data = request.json
        print(data)

        try:
            comment_id = data["entry"][0]["changes"][0]["value"]["id"]

            requests.post(
                f"https://graph.facebook.com/v25.0/{comment_id}/replies",
                params={
                    "message":"Test cevap",
                    "access_token":TOKEN
                }
            )

        except Exception as e:
            print(e)

        return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
