from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")

VERIFY_TOKEN = "yapaycevapla123"


@app.route("/")
def home():
    return "Bot aktif"


@app.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "fail"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    try:

        comment = data['entry'][0]['changes'][0]['value']['text']
        comment_id = data['entry'][0]['changes'][0]['value']['id']

        ai = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role":"system",
                    "content":
                    "Türkçe cevap veren yardımcı bir yapay zeka botsun."
                },

                {
                    "role":"user",
                    "content":comment
                }

            ]

        )

        answer = ai.choices[0].message.content

        requests.post(

            f"https://graph.facebook.com/v19.0/{comment_id}/replies",

            data={

                "message":answer,
                "access_token":INSTAGRAM_TOKEN

            }

        )

    except Exception as e:

        print(e)

    return "ok"
