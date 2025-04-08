from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                             QTextEdit, QLineEdit, QPushButton, QLabel,
                             QListWidget, QHBoxLayout, QSizePolicy, QFrame, 
                             QMessageBox, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.core.api_client import ApiClient
from app.core.ws_client import WebSocketClient
from app.core.settings import Settings

from .visitor_details_dialog import VisitorDetailsDialog
from .connection_dialog import ConnectionDialog
from .search_dialog import SearchDialog

from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ask_for_connection()

        self.setup_ui()
        self.setup_clients()
        self.connect_signals()
        self.force_sync()

    def setup_ui(self):
        self.setWindowTitle("Visitor Management Client")
        self.setMinimumSize(800, 600)
        self.setGeometry(100, 100, 800, 600)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        self.ws_status_label = QLabel("Disconnected")

        self.search_button = QPushButton("Search Visitors")
        self.add_button = QPushButton("Add Visitor")
        self.sync_button = QPushButton("Force Sync")
        button_height = 40
        self.search_button.setFixedHeight(button_height)
        self.sync_button.setFixedHeight(button_height)
        self.add_button.setFixedHeight(button_height)

        font = QFont()
        font.setPointSize(13)
        self.visitors_list = QListWidget(self)
        self.visitors_list.setFont(font)
        self.visitors_list.setAlternatingRowColors(True)
        self.visitors_list.setSelectionMode(QListWidget.SingleSelection)
        self.visitors_list.setMinimumHeight(300)

        self.visitors_list.clicked.connect(self.on_visitor_clicked)

        self.log.setStyleSheet("background-color: #1c1c1c; color: #dcdcdc;")

        layout = QVBoxLayout()

        layout.addWidget(self.ws_status_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.sync_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        layout.addWidget(QLabel("Visitors Inside:"))
        layout.addWidget(self.visitors_list)
        layout.addWidget(self.log)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_clients(self):
        self.ws_client = WebSocketClient()
        self.api_client = ApiClient.get_instance()
        self.ws_client.connect(Settings.get_ws_url())

    def connect_signals(self):
        self.api_client.response_received.disconnect()
        self.ws_client.message_received.connect(self.handle_ws_message)
        self.ws_client.connected.connect(self.handle_connect)
        self.ws_client.disconnected.connect(self.handle_disconnect)

        self.api_client.response_received.connect(self.handle_api_response)
        self.api_client.error_occurred.connect(self.log_error)

        self.search_button.clicked.connect(self.open_search_dialog)
        self.sync_button.clicked.connect(self.force_sync)

    def handle_ws_message(self, message: str):
        self.write_to_log(message)
        if "sync" in message.lower():
            self.api_client.response_received.disconnect()
            self.api_client.response_received.connect(self.handle_get_visitors)
            self.api_client.get_visitors_inside()

    def handle_api_response(self, response: dict):
        self.write_to_log("API Response:")
        self.write_to_log(str(response))

        if response and isinstance(response, list):
            self.update_visitors_list(response)

    def log_error(self, error: str):
        self.write_to_log(f"Error: {error}")

    def force_sync(self):
        self.write_to_log("Manual sync initiated...")
        self.api_client.get_visitors_inside()

    def open_search_dialog(self):
        dialog = SearchDialog()
        dialog.exec()

    def handle_get_visitors(self, response):
        if response and isinstance(response, list):
            self.write_to_log(response)
            self.update_visitors_list(response)
        else:
            self.visitors_list.clear()

    def update_visitors_list(self, visitors):
        """Update the visitors list with those currently inside."""
        self.visitors_list.clear()
        if len(visitors)>0: 
            for visitor in visitors:
                display_name = f"{visitor['visitorid']} - {visitor['name']}"
                self.visitors_list.addItem(display_name)

    def on_visitor_clicked(self):
        """Handle visitor item click."""
        selected_item = self.visitors_list.currentItem()
        if selected_item:
            visitor_id = selected_item.text().split(' - ')[0]
            self.show_visitor_details(visitor_id)

    def show_visitor_details(self, visitor_id):
        """Show visitor details in a new dialog."""
        self.api_client.response_received.disconnect()
        self.api_client.response_received.connect(self.handle_visitor_details)
        self.api_client.get_visitor_by_id(visitor_id)

    def handle_visitor_details(self, results):
        """Handle the visitor details response."""
        if results and 'visitor' in results:
            visitor_details_dialog = VisitorDetailsDialog(results['visitor'], self)
            visitor_details_dialog.exec()

    def ask_for_connection(self):
        pass
        dialog = ConnectionDialog()
        if dialog.exec():
            address = dialog.get_address()
            if address:
                Settings.set_url(address)

    def handle_connect(self):
        msg = f"Connected to {Settings.get_base_url()}"
        self.write_to_log(msg)
        self.ws_status_label.setText(msg)

    def handle_disconnect(self):
        self.write_to_log("Connection Lost")
        self.ws_status_label.setText("WebSocket Disconnected")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Connection Lost")
        msg.setText("Please ensure your network is active and the server is accessible.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

        QApplication.quit()

    def write_to_log(self, message:str):
        now = datetime.now()
        self.log.append(f"{now} - {message}")
