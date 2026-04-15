from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Gelen Ham Data:", data)

    try:
        if "entry" in data:
            for entry in data["entry"]:
                # 1. SENARYO: DM veya Hikaye Paylaşımı (Senin logundaki durum)
                if "messaging" in entry:
                    for msg_event in entry["messaging"]:
                        sender_id = msg_event["sender"]["id"]
                        
                        # Eğer mesaj metni varsa (veya paylaşılan bir postun başlığı)
                        message_data = msg_event.get("message", {})
                        text = message_data.get("text", "")
                        
                        # Senin logunda text boş gelebilir çünkü 'attachments' içinde paylaşım var
                        if not text and "attachments" in message_data:
                            # Paylaşılan postun title'ını soru olarak alabiliriz
                            text = message_data["attachments"][0].get("payload", {}).get("title", "")

                        if text:
                            print(f"DM/Share Tespit Edildi: {text}")
                            handle_response(sender_id, text, is_dm=True)

                # 2. SENARYO: Normal Yorumlar ve Mentions (Alt yapıdaki changes yapısı)
                if "changes" in entry:
                    for change in entry["changes"]:
                        value = change.get("value", {})
                        comment_id = value.get("id")
                        text = value.get("text", "")

                        if comment_id and text:
                            print(f"Yorum/Mention Tespit Edildi: {text}")
                            handle_response(comment_id, text, is_dm=False)

    except Exception as e:
        print("Sistem Hatası:", e)

    return "ok"

def handle_response(target_id, user_text, is_dm=False):
    # Kendi ismimizi içeren mesajlara cevap vermeyelim (sonsuz döngü engelleme)
    if "YapayCevapla" in user_text:
        return

    # OpenAI süreci
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sen samimi bir Instagram asistanısın. Türkçe, kısa ve net cevap ver."},
            {"role": "user", "content": user_text}
        ]
    )
    answer = completion.choices[0].message.content

    # Cevap Gönderme
    if is_dm:
        # DM olarak yanıt dön (Mesaj gönderen kişiye)
        url = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}"
        payload = {
            "recipient": {"id": target_id},
            "message": {"text": answer}
        }
    else:
        # Yorum olarak yanıt dön
        url = f"https://graph.facebook.com/v21.0/{target_id}/replies?access_token={PAGE_TOKEN}"
        payload = {"message": answer}

    res = requests.post(url, json=payload)
    print(f"Yanıt Gönderildi. Durum: {res.status_code}")

# Flask verify_token kısmı aynı kalacak...
