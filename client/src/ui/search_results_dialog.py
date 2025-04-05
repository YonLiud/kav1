from PySide6.QtWidgets import (
    QDialog, QLabel, QWidget, QVBoxLayout, QFrame, 
    QScrollArea, QPushButton, QGridLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from datetime import datetime

from ui.visitor_details_dialog import VisitorDetailsDialog

class ClickableVisitorCard(QFrame):
    def __init__(self, visitor_data):
        super().__init__()
        self.visitor_data = visitor_data
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout()
        
        # Header with name
        name_label = QLabel(self.visitor_data["name"])
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Dynamic fields (show 2-3 important ones)
        fields_to_show = [
            ('visitorId', 'ID'),
            ('inside', 'Status', lambda x: 'Inside' if x else 'Not Present'),
            ('meta.company', 'Company')
        ]
        
        for field in fields_to_show:
            value = self.get_nested_value(self.visitor_data, field[0])
            if len(field) > 2 and callable(field[2]):
                value = field[2](value)
                
            label_text = f"<b>{field[1]}:</b> {value}"
            label = QLabel(label_text)
            
            if field[0] == 'inside':
                is_inside = bool(self.visitor_data['inside'])
                label.setStyleSheet(f"""
                    color: {'#27ae60' if is_inside else '#e74c3c'};
                    font-weight: bold;
                """)
                
            layout.addWidget(label)
        
        self.setLayout(layout)
        self.setFixedHeight(140)
        self.setStyleSheet("""
            ClickableVisitorCard {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 12px;
                margin: 5px;
                border: 1px solid #dee2e6;
            }
            ClickableVisitorCard:hover {
                background-color: #e9ecef;
                border: 2px solid #3498db;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
        """)
    
    def get_nested_value(self, data, key):
        keys = key.split('.')
        for k in keys:
            data = data.get(k, {})
        return data if data != {} else "N/A"
    
    def mousePressEvent(self, event):
        # Call your existing VisitorDetailsDialog
        dialog = VisitorDetailsDialog(self.visitor_data)
        dialog.exec()
        super().mousePressEvent(event)

class SearchResultsDialog(QDialog):
    def __init__(self, search, results):
        super().__init__()
        self.setWindowTitle(f"Visitor Search Results - {search}")
        self.setMinimumSize(600, 500)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Results header
        results_header = QLabel(f"Found {len(results)} visitor(s):")
        results_header.setFont(QFont("Arial", 12, QFont.Bold))
        results_header.setStyleSheet("color: #495057; margin-bottom: 10px;")
        
        # Scrollable results area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignTop)
        container_layout.setSpacing(10)
        
        for visitor in results:
            card = ClickableVisitorCard(visitor)
            container_layout.addWidget(card)
        
        container.setLayout(container_layout)
        scroll.setWidget(container)
        
        main_layout.addWidget(results_header)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QScrollArea {
                border: none;
            }
        """)