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
    return "AI bot aktif - Mentions & Comments Destekleniyor"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "fail"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Debug için gelen veriyi loglayalım
    print("Gelen Data:", data)

    try:
        if "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    field = change.get("field")
                    value = change.get("value", {})
                    
                    # 1. Kendi postundaki yorum mu yoksa başkasının postundaki mention mı?
                    comment_id = value.get("id")
                    text = value.get("text", "")
                    
                    if not text or not comment_id:
                        continue

                    # Kendi botumuzun cevabına cevap vermeyelim
                    if "YapayCevapla" in text:
                        continue

                    # Mention kontrolü
                    if "@yapaycevapla" not in text.lower():
                        continue

                    print(f"İşleniyor ({field}): {text}")

                    # 2. OpenAI Yanıt Oluşturma
                    question = text.lower().replace("@yapaycevapla", "").strip()
                    
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini", # Model adını güncelledim
                        messages=[
                            {"role": "system", "content": "Sen bir Instagram asistanısın. Kısa, samimi ve Türkçe cevap ver. Max 2 cümle."},
                            {"role": "user", "content": question}
                        ]
                    )
                    answer = completion.choices[0].message.content

                    # 3. Cevap Gönderme
                    # Not: Mention veya Comment fark etmeksizin reply/comments endpointi kullanılır
                    url = f"https://graph.facebook.com/v21.0/{comment_id}/replies"
                    
                    payload = {
                        "message": answer,
                        "access_token": PAGE_TOKEN
                    }

                    response = requests.post(url, json=payload)
                    print(f"Cevap Durumu: {response.status_code}, Yanıt: {response.text}")

    except Exception as e:
        print("Sistem Hatası:", e)

    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
