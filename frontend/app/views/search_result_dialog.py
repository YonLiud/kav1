from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel

class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Results")

        self.layout = QVBoxLayout(self)

        # Displaying a message if there are no results
        if not results:
            self.no_results_label = QLabel("No visitors found.", self)
            self.layout.addWidget(self.no_results_label)
            return

        # Creating a list widget to show the results
        self.results_list = QListWidget(self)
        self.layout.addWidget(self.results_list)

        # Adding visitors to the list widget
        for visitor in results:
            display_name = f"{visitor['visitorid']} - {visitor['name']}"  # Display ID and Name
            self.results_list.addItem(display_name)

        # You can add more widgets or customize the layout as needed
