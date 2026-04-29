from flask import Flask, request, jsonify
from services.ocr import extract_text_from_image
from services.extractor import structure_data
from services.iron import generate_contract
from services.whatsapp import send_document, download_media
import os, logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/webhook", methods=["GET"])
def verify():
    mode  = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403
  
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        entry   = data["entry"][0]
        changes = entry["changes"][0]["value"]
        message = changes["messages"][0]

        if message["type"] == "image":
            phone  = message["from"]
            img_id = message["image"]["id"]

            img_bytes = download_media(img_id)
            raw_text  = extract_text_from_image(img_bytes)
            client    = structure_data(raw_text)
            docx_path = generate_contract(client)
            send_document(phone, docx_path,
                          caption="Seu contrato está pronto!")
          
 return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.error(f"Erro no webhook: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
