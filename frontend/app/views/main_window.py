from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                             QTextEdit, QLineEdit, QPushButton, QLabel)
from app.core.ws_client import WebSocketClient
from app.core.api_client import ApiClient
from app.core.settings import Settings

from .search_dialog import SearchDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_clients()
        self.connect_signals()

    def setup_ui(self):
        self.setWindowTitle("Visitor Management Client")
        self.setMinimumSize(800,600)
        self.setGeometry(100, 100, 800, 600)
        
        # Widgets
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search Visitors")
        self.sync_button = QPushButton("Force Sync")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.log)
        layout.addWidget(QLabel("Search Visitors:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.sync_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_clients(self):
        self.ws_client = WebSocketClient()
        self.api_client = ApiClient.get_instance()
        self.ws_client.connect(Settings.get_ws_url())

    def connect_signals(self):
        # WebSocket signals
        self.ws_client.message_received.connect(self.handle_ws_message)
        self.ws_client.connected.connect(lambda: self.log.append("WebSocket Connected"))
        self.ws_client.disconnected.connect(lambda: self.log.append("WebSocket Disconnected"))
        
        # API signals
        self.api_client.response_received.connect(self.handle_api_response)
        self.api_client.error_occurred.connect(self.log_error)
        
        # Button signals
        self.search_button.clicked.connect(self.open_search_dialog)
        self.sync_button.clicked.connect(self.force_sync)

    def handle_ws_message(self, message: str):
        self.log.append(message)
        if "sync" in message.lower():
            self.api_client.get_visitors()

    def handle_api_response(self, response: dict):
        self.log.append("API Response:")
        self.log.append(str(response))

    def log_error(self, error: str):
        self.log.append(f"Error: {error}")

    # def search_visitors(self):
    #     query = self.search_input.text()
    #     if query:
    #         self.api_client.search_visitors(query)

    def force_sync(self):
        self.log.append("Manual sync initiated...")
        self.api_client.get_visitors()

    def open_search_dialog(self):
        dialog = SearchDialog()
        dialog.exec()