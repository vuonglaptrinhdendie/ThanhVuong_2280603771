import sys
import os

# Add LAB_03 directory to sys.path to allow "from ui.rsa import Ui_MainWindow"
# This script is in LAB_03/cipher/rsa/
# We want to add LAB_03/ to sys.path
current_script_dir = os.path.dirname(os.path.abspath(__file__))
lab_03_dir = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
if lab_03_dir not in sys.path:
    sys.path.insert(0, lab_03_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Added RSACipher class definition
class RSACipher:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        
        # Xác định đường dẫn đến thư mục chứa tệp rsa_cipher.py này
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # Tạo đường dẫn đến thư mục keys bên trong thư mục hiện tại (cipher/rsa/keys)
        self.keys_dir = os.path.join(current_file_dir, "keys")
        
        os.makedirs(self.keys_dir, exist_ok=True) 
        self.private_key_path = os.path.join(self.keys_dir, "private.pem")
        self.public_key_path = os.path.join(self.keys_dir, "public.pem")

    def generate_keys(self):
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()

        with open(self.private_key_path, "wb") as f:
            f.write(self.private_key.export_key('PEM'))
        with open(self.public_key_path, "wb") as f:
            f.write(self.public_key.export_key('PEM'))
        print(f"Keys generated and saved to {self.private_key_path} and {self.public_key_path}")

    def load_keys(self):
        if not self.private_key and os.path.exists(self.private_key_path):
            with open(self.private_key_path, "rb") as f:
                self.private_key = RSA.import_key(f.read())
        if not self.public_key and os.path.exists(self.public_key_path):
            with open(self.public_key_path, "rb") as f:
                self.public_key = RSA.import_key(f.read())
        
        if not self.private_key or not self.public_key:
            print(f"Keys not found at {self.private_key_path} or {self.public_key_path}, generating new keys...")
            self.generate_keys()
            
        return self.private_key, self.public_key

    def encrypt(self, message: str, rsa_key_object: RSA.RsaKey):
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        cipher_rsa = PKCS1_OAEP.new(rsa_key_object)
        encrypted_message = cipher_rsa.encrypt(message)
        return encrypted_message

    def decrypt(self, ciphertext: bytes, rsa_key_object: RSA.RsaKey):
        cipher_rsa = PKCS1_OAEP.new(rsa_key_object)
        decrypted_message = cipher_rsa.decrypt(ciphertext)
        return decrypted_message.decode('utf-8')

    def sign(self, message: str, private_key_obj: RSA.RsaKey):
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        if not private_key_obj:
            if not self.private_key: self.load_keys()
            private_key_obj = self.private_key
        
        if not private_key_obj:
            raise ValueError("Private key not available for signing.")

        hash_obj = SHA256.new(message)
        signature = pkcs1_15.new(private_key_obj).sign(hash_obj)
        return signature

    def verify(self, message: str, signature: bytes, public_key_obj: RSA.RsaKey):
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        if not public_key_obj:
            if not self.public_key: self.load_keys()
            public_key_obj = self.public_key

        if not public_key_obj:
            raise ValueError("Public key not available for verification.")

        hash_obj = SHA256.new(message)
        try:
            pkcs1_15.new(public_key_obj).verify(hash_obj, signature)
            return True
        except (ValueError, TypeError):
            return False

# Ensure Ui_MainWindow is correctly imported if MyApp needs it.
# It might be from a generated file like 'from .ui.rsa_ui import Ui_MainWindow' or similar.
# For now, I'm commenting it out from the top and assuming it's handled if MyApp is used.
# If you have a ui/rsa.py that defines Ui_MainWindow, make sure the import is correct.
# For example: from ui.rsa import Ui_MainWindow (if ui is a package at the same level as cipher)
# Or if rsa.py is ui_rsa.py: from .ui_rsa import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5001/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data.get("message", "Keys generated successfully!")) # Use .get for safety
                msg.exec_()
            else:
                print(f"Error while calling API. Status Code: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data.get('error', response.text)}")
                    msg_text = f"API Error: {error_data.get('error', 'Unknown error from API')}"
                except ValueError: # Not a JSON response
                    print(f"Error details (non-JSON): {response.text}")
                    msg_text = f"API Error (non-JSON response): {response.status_code}"
                QMessageBox.critical(self, "API Error", msg_text)
        except requests.exceptions.RequestException as e:
            print(f"RequestException while calling API: {e}")
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5001/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5001/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5001/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5001/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                if data["is_verified"]:
                    msg.setText("Verified Successfully")
                else:
                    msg.setText("Verified Fail")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")

# ✅ KHỞI CHẠY GIAO DIỆN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
