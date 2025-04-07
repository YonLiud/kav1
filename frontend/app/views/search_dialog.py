from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QRadioButton, QPushButton, QLabel
)
from app.core.api_client import ApiClient  # Assuming ApiClient is correctly imported
from .search_result_dialog import SearchResultDialog  # Import the new result dialog

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Visitors")

        # Access the Singleton instance of ApiClient
        self.api_client = ApiClient.get_instance()  # Use get_instance to fetch the singleton

        # Set up your dialog UI
        self.layout = QVBoxLayout(self)

        self.search_label = QLabel("Enter your search query:")
        self.layout.addWidget(self.search_label)

        self.search_input = QLineEdit(self)
        self.layout.addWidget(self.search_input)

        # Radio Buttons for search type
        self.search_by_name = QRadioButton("Search by Name", self)
        self.search_by_name.setChecked(True)
        self.layout.addWidget(self.search_by_name)

        self.search_by_id = QRadioButton("Search by ID", self)
        self.layout.addWidget(self.search_by_id)

        # Button for search
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_visitors)
        self.layout.addWidget(self.search_button)

        # Connect the response_received signal to handle_search_results
        self.api_client.response_received.connect(self.handle_search_results)

    def search_visitors(self):
        query = self.search_input.text()
        if query:
            if self.search_by_name.isChecked():
                self.api_client.search_visitors(query)  # Searching by name
            elif self.search_by_id.isChecked():
                self.api_client.search_visitors(query)  # Searching by ID

            # Optionally, you can keep this dialog open until the results come back
            # self.accept()  # This can be removed if you want the dialog to stay open

    def handle_search_results(self, results):
        # Open the results in a new dialog window
        if results and 'visitors' in results:
            search_result_dialog = SearchResultDialog(results['visitors'], self)
            search_result_dialog.exec()  # Open the result dialog modally
