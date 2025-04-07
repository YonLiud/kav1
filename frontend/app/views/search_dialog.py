from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QRadioButton, QPushButton, QLabel, QMessageBox
)
from app.core.api_client import ApiClient
from .search_result_dialog import SearchResultDialog
from .visitor_details_dialog import VisitorDetailsDialog

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Visitors")

        self.api_client = ApiClient.get_instance()

        self.layout = QVBoxLayout(self)

        self.search_label = QLabel("Enter your search query:")
        self.layout.addWidget(self.search_label)

        self.search_input = QLineEdit(self)
        self.layout.addWidget(self.search_input)

        self.search_by_name = QRadioButton("Search by Name", self)
        self.search_by_name.setChecked(True)
        self.layout.addWidget(self.search_by_name)

        self.search_by_id = QRadioButton("Search by ID", self)
        self.layout.addWidget(self.search_by_id)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_visitors)
        self.layout.addWidget(self.search_button)

    def search_visitors(self):
        query = self.search_input.text()
        if query:
            if self.search_by_name.isChecked():
                self.api_client.response_received.disconnect()
                self.api_client.response_received.connect(self.handle_search_results)
                self.api_client.search_visitors(query)
            elif self.search_by_id.isChecked():
                self.api_client.response_received.disconnect()
                self.api_client.response_received.connect(self.handle_search_by_id_results)
                self.api_client.get_visitor_by_id(query)
        else:
            self.handle_empty_url()

    def handle_search_results(self, results):
        if results and 'visitors' in results:
            search_result_dialog = SearchResultDialog(results['visitors'], self)
            search_result_dialog.exec()
            self.accept()
        else:
            self.handle_no_result()
    
    def handle_search_by_id_results(self, results):
        if results and 'visitor' in results:
            visitor_details_dialog = VisitorDetailsDialog(results['visitor'], self)
            visitor_details_dialog.exec()
        else:
            self.handle_no_result()
    
    def handle_no_result(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("No Results")
        msg.setText("No matching results found.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def handle_empty_url(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Empty Prompt")
        msg.setText("Cannot search for nothing.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()