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

        text = value.get("text","")

        media_id = value["media"]["id"]

        print("COMMENT:",text)


        # kendi yorumuna cevap verme
        if "YapayCevapla" in text:
            return "ok"


        # mention yoksa cevap verme
        if "@yapaycevapla" not in text.lower():
            return "ok"


        question = text.replace("@yapaycevapla","").strip()


        # medya bilgisi çek
        media_url = ""

        try:

            media_request = requests.get(

                f"https://graph.facebook.com/v19.0/{media_id}?fields=media_type,media_url,caption&access_token={PAGE_TOKEN}"

            ).json()

            media_url = media_request.get("media_url","")

            caption = media_request.get("caption","")

        except:

            media_url = ""
            caption = ""


        # AI PROMPT
        prompt = f"""

Instagram yorumunda soru soruldu.

Soru:
{question}

Post açıklaması:
{caption}

Eğer soru ciddi ise ciddi cevap ver.
Eğer soru komik ise mizahi cevap ver.

Kısa cevap ver.
Türkçe yaz.
"""

        # Eğer resim varsa AI analiz
        if media_url != "":

            ai = client.responses.create(

                model="gpt-4.1-mini",

                input=[

                    {
                        "role":"user",
                        "content":[

                            {"type":"input_text","text":prompt},

                            {
                                "type":"input_image",
                                "image_url":media_url
                            }

                        ]
                    }

                ]

            )

        else:

            ai = client.responses.create(

                model="gpt-4.1-mini",

                input=prompt

            )


        answer = ai.output_text

        print("AI:",answer)


        # reply gönder
        url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

        payload = {

            "message":answer,
            "access_token":PAGE_TOKEN

        }

        requests.post(url,data=payload)


    except Exception as e:

        print("ERROR:",e)

    return "ok"
