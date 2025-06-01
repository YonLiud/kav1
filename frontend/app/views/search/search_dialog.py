import sys
from pathlib import Path

if __name__ == "__main__" and not __package__:
    file = Path(__file__).resolve()
    package_root = file.parents[3]
    sys.path.append(str(package_root))
    __package__ = "frontend.app.views"

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QRadioButton,
    QPushButton,
    QLabel,
    QApplication,
)
from app.core.api_client import ApiClient

from app.views.search.search_result_dialog import SearchResultDialog
from app.views.visitor.visitor_details_dialog import VisitorDetailsDialog
from app.views.common.warning_dialog import show_warning


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
                self.api_client.response_received.connect(
                    self.handle_search_by_id_results
                )
                self.api_client.get_visitor_by_id(query)
        else:
            self.handle_empty_url()

    def handle_search_results(self, results):
        if results and "visitors" in results:
            search_result_dialog = SearchResultDialog(
                self.search_input.text(), results["visitors"]
            )
            self.accept()
            search_result_dialog.exec()
        else:
            self.handle_no_result()

    def handle_search_by_id_results(self, results):
        if results and "visitor" in results:
            visitor_details_dialog = VisitorDetailsDialog(results["visitor"])
            visitor_details_dialog.exec()
        else:
            self.handle_no_result()

    def handle_no_result(self):
        show_warning(
            "Search Field Empty",
            "Please enter a search term to continue.\n\n"
            "You can search by:\n"
            "• Visitor name\n"
            "• Visitor ID\n"
            "• Date or other properties",
        )

    def handle_empty_url(self):
        show_warning(
            "No Matches Found",
            "Your search didn't return any results.\n\n"
            "Suggestions:\n"
            "• Check your spelling\n"
            "• Try a different search term\n"
            "• Verify the visitor exists in the system\n"
            "• Refresh the data if recently updated",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SearchDialog()
    dialog.show()
    sys.exit(app.exec())
