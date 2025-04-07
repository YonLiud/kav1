from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget
from PySide6.QtCore import Qt

class VisitorDetailsDialog(QDialog):
    def __init__(self, visitor_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visitor Details")

        self.layout = QVBoxLayout(self)

        self.name_label = QLabel(f"Name: {visitor_data['name']}", self)
        self.layout.addWidget(self.name_label)

        self.visitorid_label = QLabel(f"Visitor ID: {visitor_data['visitorid']}", self)
        self.layout.addWidget(self.visitorid_label)

        properties = visitor_data['properties']
        if properties:
            self.properties_label = QLabel("Properties:", self)
            self.layout.addWidget(self.properties_label)

            self.properties_list = QListWidget(self)
            for key, value in properties.items():
                self.properties_list.addItem(f"{key}: {value}")
            self.layout.addWidget(self.properties_list)
        else:
            self.no_properties_label = QLabel("No properties available.", self)
            self.layout.addWidget(self.no_properties_label)

        # Set the layout
        self.setLayout(self.layout)
