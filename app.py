from flask import Flask, request, jsonify, Response
import os

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    if token == os.getenv("VERIFY_TOKEN"):
        challenge = request.args.get("hub.challenge")
        return Response(challenge, mimetype='text/plain')  # ✅ linha 10
    return "Forbidden", 403
