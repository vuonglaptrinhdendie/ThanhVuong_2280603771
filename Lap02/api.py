from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()

# Endpoint cho Caesar Cipher - Mã hóa
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])  # Caesar dùng key là số
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

# Endpoint cho Caesar Cipher - Giải mã
@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# Endpoint cho Vigenère Cipher - Mã hóa
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']  # Vigenère dùng key là chuỗi
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

# Endpoint cho Vigenère Cipher - Giải mã
@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)