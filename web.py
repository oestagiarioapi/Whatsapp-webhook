from flask import Flask, request

app = Flask(__name__)

# Essa é a rota que o WhatsApp vai "chamar"
@app.route("/webhook", methods=['POST'])
def webhook():
    # Aqui o código recebe os dados que o WhatsApp envia
    dados = request.get_json()
    print(f"Dados recebidos: {dados}")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
