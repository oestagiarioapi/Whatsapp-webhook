from flask import Flask, request, jsonify, Response
import os

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200    
# 2. Rota do Webhook (para a Meta/Facebook validar)
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    if token == os.getenv("VERIFY_TOKEN"):
        challenge = request.args.get("hub.challenge")
        return Response(challenge, mimetype='text/plain')
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    return jsonify({"status": "ok"}), 200

