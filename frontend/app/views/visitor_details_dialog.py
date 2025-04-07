from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QFrame, 
                               QGridLayout, QScrollArea, QWidget, QPushButton)
from PySide6.QtCore import Qt

from app.core.api_client import ApiClient

class VisitorDetailsDialog(QDialog):
    def __init__(self, visitor_data, parent=None):
        super().__init__(parent)
        
        self.api_client = ApiClient.get_instance()
        
        self.visitor_data = visitor_data

        self.setWindowTitle("Visitor Details")
        self.setMinimumSize(450, 400)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)
        
        # Header Frame
        self.header_frame = QFrame()
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(12, 12, 12, 12)
        
        self.title_label = QLabel("Visitor Information")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = self.title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(14)
        self.title_label.setFont(title_font)
        header_layout.addWidget(self.title_label)
        
        self.name_label = QLabel(f"<b>Name:</b> {visitor_data['name']}")
        self.visitorid_label = QLabel(f"<b>Visitor ID:</b> {visitor_data['visitorid']}")
        self.inside_label = QLabel(f"<b>Inside:</b> {visitor_data['inside']}")
        
        header_layout.addWidget(self.name_label)
        header_layout.addWidget(self.visitorid_label)
        header_layout.addWidget(self.inside_label)
        self.layout.addWidget(self.header_frame)
        
        # Properties Frame
        self.properties_frame = QFrame()
        self.properties_frame.setFrameShape(QFrame.StyledPanel)
        properties_layout = QVBoxLayout(self.properties_frame)
        properties_layout.setContentsMargins(12, 12, 12, 12)
        
        self.properties_title = QLabel("Properties")
        self.properties_title.setAlignment(Qt.AlignCenter)
        self.properties_title.setFont(title_font)
        properties_layout.addWidget(self.properties_title)
        
        properties = visitor_data.get('properties', {})
        if properties:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QGridLayout(scroll_content)
            scroll_layout.setContentsMargins(8, 8, 8, 8)
            scroll_layout.setHorizontalSpacing(20)
            scroll_layout.setVerticalSpacing(8)
            
            for row, (key, value) in enumerate(properties.items()):
                key_label = QLabel(f"<b>{key}:</b>")
                value_label = QLabel(str(value))
                value_label.setWordWrap(True)
                scroll_layout.addWidget(key_label, row, 0)
                scroll_layout.addWidget(value_label, row, 1)
            
            scroll.setWidget(scroll_content)
            properties_layout.addWidget(scroll)
        else:
            self.no_properties_label = QLabel("No properties available.")
            self.no_properties_label.setAlignment(Qt.AlignCenter)
            properties_layout.addWidget(self.no_properties_label)
        
        self.layout.addWidget(self.properties_frame)
        
        self.toggle_button = QPushButton("Toggle Inside")
        self.toggle_button.clicked.connect(self.toggle_inside)
        self.layout.addWidget(self.toggle_button)
        
        self.layout.addStretch()

    def toggle_inside(self):
        current_id = self.visitor_data['visitorid']
        current_status = self.visitor_data['inside']
        new_status = not current_status
        print(f"{current_status} | {current_id}")
        self.api_client.update_visitor_status(current_id, new_status)
        self.accept()

        
