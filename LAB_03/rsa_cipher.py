import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Since rsa_cipher.py is now in LAB_03, the ui module is a direct subdirectory
from ui.rsa import Ui_MainWindow 
import requests

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
                msg.setText(data.get("message", "Keys generated successfully!"))
                msg.exec_()
            else:
                print(f"Error while calling API. Status Code: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data.get('error', response.text)}")
                    msg_text = f"API Error: {error_data.get('error', 'Unknown error from API')}"
                except ValueError: 
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
