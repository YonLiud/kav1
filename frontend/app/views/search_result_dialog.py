from PySide6.QtWidgets import (QDialog, QVBoxLayout, QListWidget, QLabel, 
                              QPushButton, QSizePolicy, QSpacerItem, QFrame)
from PySide6.QtCore import Qt

class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setMinimumSize(400, 300)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)
        
        # Title label
        self.title_label = QLabel("Visitor Search Results", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)
        
        # Add a separator
        self.layout.addWidget(self._create_horizontal_line())
        
        if not results:
            self.no_results_label = QLabel("No matching visitors found.", self)
            self.no_results_label.setAlignment(Qt.AlignCenter)
            self.no_results_label.setWordWrap(True)
            self.layout.addWidget(self.no_results_label)
        else:
            # Results count label
            self.results_count = QLabel(f"Found {len(results)} visitor(s):", self)
            self.layout.addWidget(self.results_count)
            
            # Results list
            self.results_list = QListWidget(self)
            self.results_list.setAlternatingRowColors(True)
            self.results_list.setSelectionMode(QListWidget.SingleSelection)
            self.layout.addWidget(self.results_list)
            
            # Add items to list
            for visitor in results:
                display_name = f"{visitor['visitorid']} - {visitor['name']}"
                self.results_list.addItem(display_name)
        
        # Add vertical spacer to push buttons down
        self.layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Add a separator
        self.layout.addWidget(self._create_horizontal_line())
        
        # Button row
        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(8)
        
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.close_button)
        
        self.layout.addLayout(self.button_layout)
    
    def _create_horizontal_line(self):
        """Helper method to create a horizontal line for visual separation"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line