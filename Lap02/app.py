from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher

app = Flask(__name__)

# Route cho trang chủ
@app.route("/")
def home():
    return render_template("index.html")

# Route cho giao diện Caesar Cipher
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")

# Route xử lý mã hóa
@app.route("/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"""
    <p><strong>Text:</strong> {text}</p>
    <p><strong>Key:</strong> {key}</p>
    <p><strong>Encrypted Text:</strong> {encrypted_text}</p>
    """

# Route xử lý giải mã
@app.route("/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"""
    <p><strong>Text:</strong> {text}</p>
    <p><strong>Key:</strong> {key}</p>
    <p><strong>Decrypted Text:</strong> {decrypted_text}</p>
    """

# Hàm main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)