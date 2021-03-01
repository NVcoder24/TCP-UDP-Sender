from PyQt5 import QtWidgets, uic
import sys
import socket
from threading import Thread

try:
    class Ui(QtWidgets.QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            uic.loadUi('tcp_udp_sender_ui.ui', self)

            self.label_5.setText("")
            self.btn = self.findChild(QtWidgets.QPushButton, "pushButton")
            self.btn.clicked.connect(self.send)
            self.ip_ = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
            self.port_ = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
            self.data_ = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
            self.error = self.findChild(QtWidgets.QLabel, 'label_5')
            self.protocol_ = self.findChild(QtWidgets.QComboBox, "comboBox_2")
            self.data_type_ = self.findChild(QtWidgets.QComboBox, "comboBox")

            self.show()

        def send_(self):
            self.t = Thread(target=self.send).start()
            self.t = None

        def send(self):
            try:
                self.error.setText("")
                self.protocol = self.protocol_.currentText()
                self.data_type = self.data_type_.currentText()
                self.ip = self.ip_.text()
                self.port = int(self.port_.text())
                self.data = self.data_.text()

                if self.protocol == "TCP":
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.sock.connect((self.ip, self.port))
                    if self.data_type == "string":
                        self.byt = bytes(str(self.data), "utf-8")
                        self.sock.send(self.byt)
                    elif self.data_type == "int":
                        self.byt = bytes(str(int(self.data)), "utf-8")
                        self.sock.send(self.byt)
                    elif self.data_type == "bool":
                        self.byt = bytes(str(bool(self.data)), "utf-8")
                        self.sock.send(self.byt)
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()

                elif self.protocol == "UPD":
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.sock.connect((self.ip, self.port))
                    if self.data_type == "string":
                        self.byt = bytes(str(self.data), "utf-8")
                        self.sock.send(self.byt)
                    elif self.data_type == "int":
                        self.byt = bytes(str(int(self.data)), "utf-8")
                        self.sock.send(self.byt)
                    elif self.data_type == "bool":
                        self.byt = bytes(str(bool(self.data)), "utf-8")
                        self.sock.send(self.byt)
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()

                self.sock = None

            except Exception as e:
                print(f"error: {e}")
                try:
                    self.error.setText(f"error: {e}")
                except Exception as e:
                    print(e)

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
except Exception as e:
    print(f"FATAL ERROR: {e}")
    quit()