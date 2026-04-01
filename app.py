from flask import Flask, request
import requests
import os
import openai

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")

VERIFY_TOKEN = "yapaycevapla123"

@app.route("/")
def home():
    return "YapayCevapla Bot Aktif"

@app.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    try:

        comment = data['entry'][0]['changes'][0]['value']['text']
        comment_id = data['entry'][0]['changes'][0]['value']['id']

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role":"system",
                    "content":
                    "Sen YapayCevapla AI botusun. Türkçe cevap ver. "
                    "Kibar, profesyonel ve yardımcı ol. "
                    "Bilmediğin şeyi tahmin olarak belirt."
                },
                {
                    "role":"user",
                    "content":comment
                }
            ]
        )

        answer = response.choices[0].message.content

        url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

        requests.post(url,data={
            "message":answer,
            "access_token":INSTAGRAM_TOKEN
        })

    except Exception as e:
        print(e)

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
