from flask import Flask, request, jsonify, Response
import os

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200    
# 2. Rota do Webhook (para a Meta/Facebook validar)
@app.route("/webhook", methods=["GET"])
def webhook():
    token = request.args.get("hub.verify_token")
    if token == os.getenv("VERIFY_TOKEN"):
        challenge = request.args.get("hub.challenge")
        return Response(challenge, mimetype='text/plain')
    return "Forbidden", 403

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
