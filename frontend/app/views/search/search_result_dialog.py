from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QFrame)
from PySide6.QtCore import Qt

from app.core.api_client import ApiClient
from app.views.visitor.visitor_details_dialog import VisitorDetailsDialog
from app.views.common.warning_dialog import show_warning


class SearchResultDialog(QDialog):
    def __init__(self, query, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setMinimumSize(400, 300)
        self.api_client = ApiClient.get_instance()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)

        self.title_label = QLabel(f'"{query}" Search Results', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)

        self.layout.addWidget(self._create_horizontal_line())

        if not results:
            self.no_results_label = QLabel("No matching visitors found.", self)
            self.no_results_label.setAlignment(Qt.AlignCenter)
            self.no_results_label.setWordWrap(True)
            self.layout.addWidget(self.no_results_label)
        else:
            self.results_count = QLabel(
                f"Found <b>{len(results)}</b> visitor(s):", self)
            self.layout.addWidget(self.results_count)

            self.results_list = QListWidget(self)
            self.results_list.setAlternatingRowColors(True)
            self.results_list.setSelectionMode(QListWidget.SingleSelection)
            self.layout.addWidget(self.results_list)

            for visitor in results:
                display_name = f"{visitor['visitorid']} - {visitor['name']}"
                self.results_list.addItem(display_name)

            self.results_list.itemClicked.connect(self.on_item_clicked)

        self.layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum,
                                        QSizePolicy.Expanding))

        self.layout.addWidget(self._create_horizontal_line())

        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(8)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)
        self.close_button.setFocusPolicy(Qt.NoFocus)
        self.button_layout.addWidget(self.close_button)

        self.layout.addLayout(self.button_layout)

    def _create_horizontal_line(self):
        """Helper method to create a horizontal line for visual separation"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def search_details(self, visitorid: str):
        self.api_client.response_received.disconnect()
        self.api_client.response_received.connect(
            self.handle_search_details_result)
        self.api_client.get_visitor_by_id(visitorid)

    def handle_search_details_result(self, results):
        if results and 'visitor' in results:
            visitor_details_dialog = VisitorDetailsDialog(results['visitor'],
                                                          self)
            visitor_details_dialog.exec()
        else:
            show_warning(
                "Visitor Not Found",
                "The requested visitor could not be found.\n"
                "The visitor may have been deleted.\n"
                "Check the ID for typos.\n"
                "Try force syncing."
            )

    def on_item_clicked(self, item):
        """Handle item click event"""
        visitorid = item.text().split(' - ')[0]
        self.search_details(visitorid)
