from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
from PySide6.QtCore import Qt

class ServerChangeDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Server")
        self.setFixedSize(200, 100)

        layout = QFormLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("ws://127.0.0.1:3000")
        layout.addRow(self.url_input)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect_clicked)
        layout.addRow(self.connect_button)

        self.setLayout(layout)

        self.url = ""

    def on_connect_clicked(self):
        self.url = self.url_input.text().strip()
        if not self.url:
            QMessageBox.warning(self, "Input Error", "The server URL cannot be empty. Using default...")
            self.url= "ws://localhost:3000"
            self.accept()
        else:
            self.accept()

    def get_url(self):
        return self.url
    