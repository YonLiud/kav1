from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QFrame, 
                               QLineEdit, QSizePolicy, QScrollArea, QWidget, 
                               QPushButton, QStyle, QMessageBox)
from PySide6.QtCore import Qt

from app.core.api_client import ApiClient
from app.utils.log import Log

class VisitorDetailsDialog(QDialog):
    def __init__(self, visitor_data, parent=None):
        super().__init__(parent)
        
        self.api_client = ApiClient.get_instance()
        self.logger = Log()
        
        self.visitor_data = visitor_data

        self.setWindowTitle("Visitor Details")
        self.setMinimumSize(450, 400)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)
        
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
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setContentsMargins(8, 8, 8, 8)
            scroll_layout.setSpacing(8)

            for key, value in properties.items():
                line_edit = QLineEdit()
                line_edit.setText(f"{key}: {value}")
                line_edit.setAlignment(Qt.AlignLeft) 
                line_edit.setReadOnly(True)
                line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                line_edit.adjustSize()

                scroll_layout.addWidget(line_edit)

            scroll.setWidget(scroll_content)
            properties_layout.addWidget(scroll)
        else:
            self.no_properties_label = QLabel("No properties available.")
            self.no_properties_label.setAlignment(Qt.AlignCenter)
            properties_layout.addWidget(self.no_properties_label)
                
        self.layout.addWidget(self.properties_frame)

        isInside = self.visitor_data["inside"]
        self.logger.write_to_log(isInside)
        self.logger.write_to_log(type(isInside))

        self.toggle_button = QPushButton(f"Mark {'Outside' if isInside else 'Inside'}")
        button_height = 40
        self.toggle_button.setMinimumHeight(button_height)
        self.toggle_button.setIcon(self.style().standardIcon(QStyle.SP_VistaShield))
        self.toggle_button.clicked.connect(self.toggle_inside)
        self.layout.addWidget(self.toggle_button)

        # Delete button
        self.delete_button = QPushButton("Delete Visitor")
        self.delete_button.setMinimumHeight(button_height)
        self.delete_button.clicked.connect(self.delete_visitor)
        self.layout.addWidget(self.delete_button)

        self.layout.addStretch()

    def toggle_inside(self):
        current_id = self.visitor_data['visitorid']
        current_status = self.visitor_data['inside']
        new_status = not current_status
        self.logger.write_to_log(f"{current_status} | {current_id}")
        self.api_client.update_visitor_status(current_id, new_status)
        self.accept()

    def delete_visitor(self):
        """Delete the visitor after confirmation by calling the API."""
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                    "Are you sure you want to delete this visitor?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logger.write_to_log(f"Deleting visitor with ID: {self.visitor_data['visitorid']}")
            self.api_client.delete_visitor(visitor_id=self.visitor_data['visitorid'])
            self.accept()
        else:
            pass