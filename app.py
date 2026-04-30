from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    if token == os.getenv("VERIFY_TOKEN"):
        return request.args.get('hub.challenge'), mimetype='text/plain'
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    # seu processamento aqui
    return jsonify({"status": "ok"}), 200
