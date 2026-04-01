from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

VERIFY_TOKEN = "yapaycevapla123"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    try:
        comment = data['entry'][0]['changes'][0]['value']['text']
        comment_id = data['entry'][0]['changes'][0]['value']['id']

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"system","content":"Sen YapayCevapla AI botusun. Türkçe cevap ver. Kibar, profesyonel ve yardımcı ol."},
                {"role":"user","content":comment}
            ]
        )

        answer = response.choices[0].message.content

        url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

        requests.post(url, data={
            "message":answer,
            "access_token":INSTAGRAM_TOKEN
        })

    except Exception as e:
        print(e)

    return "ok"

import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
