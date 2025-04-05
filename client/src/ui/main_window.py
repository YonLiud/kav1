import asyncio
from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QHBoxLayout
)
import json
from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QCursor
from ui.server_change_dialog import ServerChangeDialog
from ui.search_visitor_dialog import SearchVisitorDialog
from ui.visitor_form_dialog import VisitorFormDialog
from ui.visitor_details_dialog import VisitorDetailsDialog
from ui.search_results_dialog import SearchResultsDialog
from websocket.client import WebSocketClient

class MainWindow(QMainWindow):
    def __init__(self, appName="KAV1"):
        super().__init__()
        self.websocket_client = WebSocketClient()
        self.current_visitors = []
        
        self.setup_ui(appName)
        self.setup_websocket_signals()

    def setup_ui(self, appName):
        self.setWindowTitle(appName)
        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(800, 600)
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        self.layout = QVBoxLayout(main_widget)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Connection status
        self.connection_status = QLabel("Disconnected")
        self.connection_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.connection_status)

        # Visitors table
        self.setup_visitors_table()

        # Button row
        self.setup_buttons()

    def setup_visitors_table(self):
        """Setup the visitors table with clickable rows"""
        self.visitors_table = QTableWidget()
        self.visitors_table.setColumnCount(5)
        self.visitors_table.setHorizontalHeaderLabels([
            "Name", "Visitor ID", "Company", "Department", "Status"
        ])
        self.visitors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.visitors_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.visitors_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.visitors_table.cellDoubleClicked.connect(self.show_visitor_details)
        
        # Style for clickable rows
        self.visitors_table.setCursor(QCursor(Qt.PointingHandCursor))
        self.layout.addWidget(self.visitors_table)

    def setup_buttons(self):
        """Setup all control buttons"""
        button_layout = QHBoxLayout()
        
        # Connection button
        self.connect_button = QPushButton("Connect to Server")
        self.connect_button.clicked.connect(self.toggle_connection)
        button_layout.addWidget(self.connect_button)

        # Search button
        self.search_button = QPushButton("Search Visitor")
        self.search_button.clicked.connect(self.ask_for_name)
        button_layout.addWidget(self.search_button)

        # Add visitor button
        self.add_visitor_button = QPushButton("Add Visitor")
        self.add_visitor_button.clicked.connect(self.ask_for_visitor)
        button_layout.addWidget(self.add_visitor_button)

        # Visitor details button
        self.details_button = QPushButton("Visitor Details")
        self.details_button.clicked.connect(self.show_selected_visitor_details)
        button_layout.addWidget(self.details_button)

        # Search results button
        self.results_button = QPushButton("Search Results")
        self.results_button.clicked.connect(self.pretend_search_results)
        button_layout.addWidget(self.results_button)

        self.layout.addLayout(button_layout)

    def setup_websocket_signals(self):
        self.websocket_client.connected.connect(self.on_connected)
        self.websocket_client.disconnected.connect(self.on_disconnected)
        self.websocket_client.error_occurred.connect(self.on_error)
        self.websocket_client.visitors_updated.connect(self.update_visitors_table)

    @Slot()
    def on_connected(self):
        """Handle successful connection"""
        self.connection_status.setText(f"Connected to {self.websocket_client.connected_url}")
        self.connection_status.setStyleSheet("color: green;")
        self.connect_button.setText("Disconnect")
        # Request and display visitors
        asyncio.create_task(self.fetch_and_display_visitors())

    async def fetch_and_display_visitors(self):
        """Fetch visitors and update table"""
        visitors = await self.websocket_client.get_visitors_inside()
        if visitors is not None:
            self.update_visitors_table(visitors)
        else:
            QMessageBox.warning(self, "Warning", "Could not fetch visitor data")

    @Slot()
    def on_disconnected(self):
        self.connection_status.setText("Disconnected")
        self.connection_status.setStyleSheet("color: red;")
        self.connect_button.setText("Connect to Server")
        self.clear_visitors_table()

    @Slot(str)
    def on_error(self, error):
        QMessageBox.critical(self, "WebSocket Error", error)

    @Slot(list)
    def update_visitors_table(self, visitors):
        """Update table with visitor data"""
        try:
            print("Updating table with visitors:", len(visitors))  # Debug
            self.visitors_table.setRowCount(0)  # Clear existing rows
            
            if not visitors:
                print("No visitors received")
                return

            self.visitors_table.setRowCount(len(visitors))
            for row, visitor in enumerate(visitors):
                # Handle meta field (could be string or dict)
                meta = visitor.get('meta', {})
                if isinstance(meta, str):
                    try:
                        meta = json.loads(meta)
                    except:
                        meta = {}

                # Handle inside status (could be 0/1, true/false, or string)
                inside = visitor.get('inside', False)
                if isinstance(inside, str):
                    inside = inside.lower() in ('true', '1', 'yes')
                else:
                    inside = bool(inside)

                # Set items in the table
                self.visitors_table.setItem(row, 0, QTableWidgetItem(visitor.get('name', '')))
                self.visitors_table.setItem(row, 1, QTableWidgetItem(visitor.get('visitorId', '')))
                self.visitors_table.setItem(row, 2, QTableWidgetItem(meta.get('company', '')))
                self.visitors_table.setItem(row, 3, QTableWidgetItem(meta.get('department', '')))
                
                status_item = QTableWidgetItem("Inside" if inside else "Outside")
                status_item.setForeground(Qt.green if inside else Qt.red)
                status_item.setData(Qt.UserRole, visitor)  # Store full data
                self.visitors_table.setItem(row, 4, status_item)

        except Exception as e:
            print("Error updating table:", e)
            self.error_occurred.emit(f"Display error: {str(e)}")

        except Exception as e:
            print("Error updating table:", e)
            self.error_occurred.emit(f"Display error: {str(e)}")
            self.visitors_table.setRowCount(0)

    def clear_visitors_table(self):
        """Clear the visitors table"""
        self.visitors_table.setRowCount(0)
        self.current_visitors = []

    @Slot()
    def toggle_connection(self):
        """Slot for connect/disconnect button (now synchronous)"""
        if self.websocket_client.websocket:
            asyncio.create_task(self.websocket_client.disconnect())
        else:
            dialog = ServerChangeDialog()
            if dialog.exec():
                url = dialog.get_url()
                if url:
                    asyncio.create_task(self.connect_to_server(url))

    async def connect_to_server(self, url):
        """Async method to handle connection"""
        if await self.websocket_client.connect(url):
            pass

    def show_visitor_details(self, row, column):
        """Show details when visitor row is clicked"""
        visitor_item = self.visitors_table.item(row, 0)
        if visitor_item:
            visitor = visitor_item.data(Qt.UserRole)
            self.open_visitor_details(visitor)

    def show_selected_visitor_details(self):
        """Show details for currently selected visitor"""
        selected = self.visitors_table.selectedItems()
        if selected:
            visitor = selected[0].data(Qt.UserRole)
            self.open_visitor_details(visitor)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a visitor first")

    def open_visitor_details(self, visitor):
        """Open visitor details dialog"""
        dialog = VisitorDetailsDialog(visitor)
        dialog.exec()

    def ask_for_server(self):
        """Legacy method kept for compatibility"""
        asyncio.create_task(self.toggle_connection())

    def ask_for_name(self):
        """Open search visitor dialog"""
        dialog = SearchVisitorDialog()
        if dialog.exec():
            name = dialog.get_name()
            print(f"Search Name: {name}")

    def ask_for_visitor(self):
        """Open add visitor dialog"""
        fields = [
            "Email", "Phone Number", "Purpose of Visit", "Date of Visit", 
            "Time of Visit", "Visitor Type", "Company Name", "Department", 
            "Host Name", "Visitor Status", "Visitor Photo", "Visitor Signature",
            "Visitor Vehicle", "Visitor Badge", "Visitor Access Level",
            "Visitor Check-in Time", "Visitor Check-out Time", "Visitor Notes", 
            "Visitor Emergency Contact"
        ]
        dialog = VisitorFormDialog(fields)
        if dialog.exec():
            submitted_json = dialog.get_submitted_json()
            if submitted_json:
                print("Submitted JSON from dialog:\n", submitted_json)
                # Here you would send this to server via WebSocket
                asyncio.create_task(self.websocket_client.create_visitor(submitted_json))

    def visitor_details(self):
        """Legacy method kept for compatibility"""
        self.show_selected_visitor_details()

    def pretend_search_results(self):
        """Demo search results dialog"""
        json_data = {
            "status": "OK",
            "code": "VISITORS_RETRIEVED",
            "message": "Visitors fetched successfully",
            "data": [
                {
                    "id": 2,
                    "name": "Emma Brown",
                    "visitorId": "VIS-M94CSA5D-IA",
                    "inside": True,
                    "meta": {
                        "company": "Wayne Ent",
                        "department": "Sales",
                        "purpose": "Consulting",
                        "badgeNumber": "B2367",
                        "lastVisit": "2025-04-04T17:13:10.753Z",
                        "visitsCount": 3,
                        "host": "host9@company.com",
                        "securityClearance": "Standard"
                    },
                    "createdAt": "2025-04-05T15:13:10.754Z",
                    "updatedAt": "2025-04-05T15:13:10.754Z"
                },
                {
                    "id": 3,
                    "name": "William Brown",
                    "visitorId": "VIS-M94CSAAW-86",
                    "inside": False,
                    "meta": {
                        "company": "Globex Corp",
                        "department": "Sales",
                        "purpose": "Delivery",
                        "badgeNumber": "B8250",
                        "lastVisit": "2025-04-04T20:13:10.952Z",
                        "visitsCount": 5,
                        "host": "host7@company.com",
                        "securityClearance": "Standard"
                    },
                    "createdAt": "2025-04-05T15:13:10.953Z",
                    "updatedAt": "2025-04-05T15:13:59.613Z"
                }
            ]
        }
        dialog = SearchResultsDialog("brown", json_data["data"])
        dialog.exec()

    def closeEvent(self, event):
        """Clean up when window is closed"""
        async def cleanup():
            if self.websocket_client.websocket:
                await self.websocket_client.disconnect()
        
        # Run cleanup synchronously
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(cleanup())
            else:
                loop.run_until_complete(cleanup())
        except RuntimeError:
            # No event loop
            pass
        
        super().closeEvent(event)