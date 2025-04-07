from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QRadioButton, QDialogButtonBox, QLabel, QListWidget
)
from PySide6.QtCore import Qt
from app.core.api_client import ApiClient  # Assuming ApiClient is correctly imported

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
        self.search_button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.search_button.accepted.connect(self.search_visitors)
        self.layout.addWidget(self.search_button)

        # List widget for displaying the search results
        self.results_list = QListWidget(self)
        self.layout.addWidget(self.results_list)

        # Connect the signal from ApiClient to the method that handles the results
        self.api_client.response_received.connect(self.handle_search_results)

    def search_visitors(self):
        query = self.search_input.text()
        if query:
            if self.search_by_name.isChecked():
                self.api_client.search_visitors(query)  # Searching by name
            elif self.search_by_id.isChecked():
                self.api_client.search_visitors(query)  # Searching by ID
            self.results_list.clear()  # Clear previous results
            self.results_list.addItem("Searching...")  # Show loading message

    def handle_search_results(self, results):
        # Check if results are valid and extract the list of visitors
        self.results_list.clear()  # Clear the loading message or previous results

        if 'visitors' in results:
            visitors = results['visitors']
            if visitors:
                for visitor in visitors:
                    display_name = f"{visitor['visitorid']} - {visitor['name']}"  # Display ID and Name
                    self.results_list.addItem(display_name)
            else:
                self.results_list.addItem("No visitors found")
        else:
            self.results_list.addItem("Error: Invalid response")
