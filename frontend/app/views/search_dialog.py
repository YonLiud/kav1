from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QLineEdit, 
    QRadioButton, QPushButton
)
from PySide6.QtCore import Qt

from app.core.api_client import ApiClient

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.api_client = ApiClient.get_instance()
        self.setWindowTitle("Search")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Enter search query:")
        layout.addWidget(self.label)

        self.search_input = QLineEdit(self)
        layout.addWidget(self.search_input)

        radio_layout = QHBoxLayout()

        self.search_by_name_radio = QRadioButton("Search by Name")
        self.search_by_name_radio.setChecked(True)
        radio_layout.addWidget(self.search_by_name_radio)

        self.search_by_id_radio = QRadioButton("Search by ID")
        radio_layout.addWidget(self.search_by_id_radio)

        layout.addLayout(radio_layout)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_visitors)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_visitors(self):
        query = self.search_input.text()
        if query:
            if self.search_by_name_radio.isChecked():
                self.api_client.search_visitors(query)
            elif self.search_by_id_radio.isChecked():
                self.api_client.search_visitors(query)

        self.accept()

if __name__ == "__main__":
    app = QApplication([])

    dialog = SearchDialog()
    dialog.exec()

    app.exec()
