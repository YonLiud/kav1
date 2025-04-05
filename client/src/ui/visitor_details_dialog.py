from PySide6.QtWidgets import (
    QDialog, QLineEdit, QFormLayout, QVBoxLayout,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

class VisitorDetailsDialog(QDialog):
    def __init__(self, visitor_data):
        super().__init__()
        self.setWindowTitle("Visitor Details")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()
        form = QFormLayout()

        flat_data = dict(visitor_data)
        if "meta" in visitor_data:
            flat_data.update(visitor_data["meta"])
            del flat_data["meta"]

        self.inputs = {}

        for key, value in flat_data.items():
            line_edit = QLineEdit(str(value))
            line_edit.setAlignment(Qt.AlignCenter)
            line_edit.setReadOnly(True)
            form.addRow(key, line_edit)
            self.inputs[key] = line_edit

        layout.addLayout(form)

        toggle_btn = QPushButton("Check Out" if visitor_data.get("inside") else "Check In")
        toggle_btn.clicked.connect(self.toggle_visitor_status)
        layout.addWidget(toggle_btn)

        self.setLayout(layout)

    def toggle_visitor_status(self):
        reply = QMessageBox.question(
            self,
            "Confirm Action",
            "Are you sure you want to toggle the visitor's status?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            print("Visitor status toggled.")
            self.accept()
        else:
            print("Visitor status not toggled.")

