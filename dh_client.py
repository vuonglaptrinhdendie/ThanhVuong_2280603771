from PyQt5 import QtWidgets
from ui.dh_exchange import Ui_MainWindow
import sys
from Crypto.PublicKey import RSA

class DHKeyExchangeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Gán sự kiện cho nút "Trao Đổi Khóa"
        self.ui.generateButton.clicked.connect(self.perform_key_exchange)

    def perform_key_exchange(self):
        # Tạo khóa RSA cho server
        server_key = RSA.generate(2048)
        server_public_pem = server_key.publickey().export_key().decode()

        # Tạo khóa RSA cho client
        client_key = RSA.generate(2048)
        client_public_pem = client_key.publickey().export_key().decode()

        # Giả lập shared secret bằng cách lấy modulus chung
        # Lưu ý: Đây chỉ là minh họa chứ không phải shared secret thực sự như trong DH
        shared_secret = hex(server_key.publickey().n ^ client_key.publickey().n)[2:]  # XOR modulus

        # Hiển thị các khóa lên giao diện
        self.ui.serverPublicKey.setPlainText(server_public_pem)
        self.ui.clientPublicKey.setPlainText(client_public_pem)
        self.ui.sharedSecret.setPlainText("Shared Secret (modulus XOR):\n" + shared_secret)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DHKeyExchangeApp()
    window.setWindowTitle("RSA Key Exchange (PEM Display)")
    window.show()
    sys.exit(app.exec_())
