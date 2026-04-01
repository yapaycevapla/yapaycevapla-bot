from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "SERVER OK"

@app.route("/webhook")
def webhook():
    return "WEBHOOK OK"
