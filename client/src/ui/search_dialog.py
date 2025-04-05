from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PySide6.QtCore import Qt

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search")
        self.setFixedSize(200, 100)

        layout = QFormLayout()

        label = QLabel("Search visitor")
        label.setAlignment(Qt.AlignCenter)
        layout.addRow(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("John Doe")
        layout.addRow(self.name_input)

        self.search_button = QPushButton("SEARCH")
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addRow(self.search_button)

        self.setLayout(layout)

    def on_search_clicked(self):
        url = self.name_input.text().strip()
        if not url:
            QMessageBox.critical(self, "Input Error", "The name cannot be empty.")
        else:
            self.accept()

    def get_name(self):
        return self.name_input.text()
    