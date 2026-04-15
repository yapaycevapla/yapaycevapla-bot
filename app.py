from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)


@app.route("/")
def home():
    return "AI bot aktif"


@app.route("/webhook", methods=["GET"])
def verify():

    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")

    return "fail"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    try:

        value = data["entry"][0]["changes"][0]["value"]

        comment_id = value["id"]
        text = value.get("text", "")

        print("COMMENT:", text)
        print("COMMENT ID:", comment_id)

        # kendi yorumuna cevap verme
        if "YapayCevapla" in text:
            return "ok"

        # mention yoksa cevap verme
        if "@yapaycevapla" not in text.lower():
            return "ok"

        question = text.replace("@yapaycevapla", "").strip()

        # AI cevap
        ai = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
Kullanıcı Instagram yorumunda soru soruyor.

Soru:
{question}

Kısa, anlaşılır, Türkçe cevap ver.
Max 2-3 cümle.
"""
        )

        answer = ai.output_text

        print("AI:", answer)

        # REPLY GÖNDER
        url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

        payload = {
            "message": answer,
            "access_token": PAGE_TOKEN
        }

        response = requests.post(url, data=payload)

        print("REPLY STATUS:", response.status_code)
        print("REPLY RESPONSE:", response.text)

    except Exception as e:

        print("ERROR:", e)

    return "ok"
