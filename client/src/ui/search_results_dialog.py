from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

class VisitorCard(QWidget):
    def __init__(self, name, visitor_id, inside):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Name: {name}"))
        layout.addWidget(QLabel(f"Visitor ID: {visitor_id}"))
        layout.addWidget(QLabel(f"Inside: {inside}"))
        self.setLayout(layout)

class SearchResultsDialog(QDialog):
    def __init__(self, results):
        super().__init__()
        self.setWindowTitle("Search Results")

        self.results_layout = QVBoxLayout()

        for visitor in results:
            card = VisitorCard(visitor["name"], visitor["visitorId"], visitor["inside"])
            self.results_layout.addWidget(card)

        self.setLayout(self.results_layout)