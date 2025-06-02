from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel
from datetime import datetime


class LogsDialog(QDialog):
    def __init__(self, logs, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logs")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()
        self.logs_list = QListWidget()

        for log in logs:
            ts = datetime.fromisoformat(log["timestamp"])
            formatted = ts.strftime("%H:%M:%S %d/%m/%Y")
            entry = f"{formatted} - {log['visitor_dbid']} - {log['visitor_name']} - {log['action']} "
            self.logs_list.addItem(entry)

        layout.addWidget(QLabel("Recent Logs:"))
        layout.addWidget(self.logs_list)
        self.setLayout(layout)
