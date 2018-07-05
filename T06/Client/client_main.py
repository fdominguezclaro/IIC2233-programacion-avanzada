import sys

from PyQt5.QtWidgets import QApplication
from frontend import MainWindow

if __name__ == "__main__":
    port = 8082
    host = '192.168.0.193'

    app = QApplication(sys.argv)
    menu = MainWindow(host, port)
    sys.exit(app.exec())
