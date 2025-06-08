import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from ui.chat import Ui_MainWindow
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket

class ReceiverThread(QThread):
    message_received = pyqtSignal(str, str)  # (sender, message)

    def __init__(self, client_socket, aes_key):
        super().__init__()
        self.client_socket = client_socket
        self.aes_key = aes_key
        self.running = True

    def decrypt_message(self, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    def run(self):
        while self.running:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break
                message = self.decrypt_message(encrypted_message)
                self.message_received.emit("", message) ###Server
            except Exception as e:
                self.message_received.emit("Error", str(e))
                break

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class ChatClient(QMainWindow):
    def __init__(self):
        super(ChatClient, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.sendButton.clicked.connect(self.send_message)
        self.ui.textEdit.setReadOnly(True)  # Sửa thành textEdit

        self.setup_connection()

        self.receiver_thread = ReceiverThread(self.client_socket, self.aes_key)
        self.receiver_thread.message_received.connect(self.append_text)
        self.receiver_thread.start()

    def setup_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

        self.client_key = RSA.generate(2048)
        self.server_public_key = RSA.import_key(self.client_socket.recv(2048))
        self.client_socket.send(self.client_key.publickey().export_key(format='PEM'))

        encrypted_aes_key = self.client_socket.recv(2048)
        cipher_rsa = PKCS1_OAEP.new(self.client_key)
        self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    def encrypt_message(self, message):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def send_message(self):
        message = self.ui.messageInput.text()
        if not message:
            return
        encrypted = self.encrypt_message(message)
        self.client_socket.send(encrypted)
        self.append_text("", message) ####
        self.ui.messageInput.clear()
        if message.lower() == "exit":
            self.client_socket.close()
            self.close()

    def append_text(self, sender, message):
        self.ui.textEdit.append(f"<b>{sender}</b> {message}")  # Sửa thành textEdit

    def closeEvent(self, event):
        if hasattr(self, 'receiver_thread'):
            self.receiver_thread.stop()
        self.client_socket.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChatClient()
    win.show()
    sys.exit(app.exec_())