# Created by samuel.martin199@outlook.com at 22/05/2023


import PySide2.QtWidgets as QtWidgets
from PySide2.QtCore import Qt

class AlertDialog(QtWidgets.QDialog):

    def __init__(self, message_text):
        super().__init__()

        self.setWindowTitle("ALERT")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        QBtn = QtWidgets.QDialogButtonBox.Ok  # | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(message_text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.exec_()
