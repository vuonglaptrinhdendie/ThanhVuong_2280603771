import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.caesar import Ui_MainWindow

class CaesarCipher:
    @staticmethod
    def encrypt(text, key):
        result = ''
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + key) % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def decrypt(text, key):
        return CaesarCipher.encrypt(text, -key)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        try:
            text = self.ui.txt_plain_text.toPlainText()
            key = int(self.ui.txt_key.text())
            result = CaesarCipher.encrypt(text, key)
            self.ui.txt_cipher_text.setText(result)
        except ValueError:
            self.ui.txt_cipher_text.setText("Invalid key")

    def decrypt_text(self):
        try:
            text = self.ui.txt_cipher_text.toPlainText()
            key = int(self.ui.txt_key.text())
            result = CaesarCipher.decrypt(text, key)
            self.ui.txt_plain_text.setText(result)
        except ValueError:
            self.ui.txt_plain_text.setText("Invalid key")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
