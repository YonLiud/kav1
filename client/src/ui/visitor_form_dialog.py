from PySide6.QtWidgets import QDialog, QLineEdit, QFormLayout, QVBoxLayout, QPushButton, QMessageBox, QWidget, QCheckBox, QScrollArea
from PySide6.QtCore import Qt
import json

class VisitorFormDialog(QDialog):
    def __init__(self, fields):
        super().__init__()

        self.setWindowTitle("Visitor Form")
        self.setMinimumSize(800, 500)
        
        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Visitor's Name")
        self.name_input.setAlignment(Qt.AlignCenter)
        self.name_input.setReadOnly(False)
        self.layout.addRow("Name:", self.name_input)

        self.visitorid_input = QLineEdit()
        self.visitorid_input.setPlaceholderText("Visitor ID")
        self.visitorid_input.setAlignment(Qt.AlignCenter)
        self.visitorid_input.setReadOnly(False)
        self.layout.addRow("Visitor ID:", self.visitorid_input)

        self.fields_inputs = {}
        for field in fields:
            field_input = QLineEdit()
            field_input.setAlignment(Qt.AlignCenter)
            field_input.setReadOnly(False)
            field_input.setPlaceholderText(f"{field}")
            self.layout.addRow(f"{field}:", field_input)
            self.fields_inputs[field] = field_input

        self.security_checkbox = QCheckBox("I confirm that the visitor is authorized to enter the premises and the information provided is accurate.")
        self.security_checkbox.setChecked(False)
        self.layout.addRow(self.security_checkbox)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit_clicked)
        self.layout.addRow(self.submit_button)

        form_container = QWidget()
        form_container.setLayout(self.layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(form_container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.submitted_data = None

    def on_submit_clicked(self):
        name = self.name_input.text()
        visitor_id = self.visitorid_input.text()
        security_agreed = self.security_checkbox.isChecked()

        if not name:
            QMessageBox.warning(self, "Input Error", "Name cannot be empty!")
            return
        if not visitor_id:
            QMessageBox.warning(self, "Input Error", "Visitor ID cannot be empty!")
            return
        if not security_agreed:
            QMessageBox.warning(self, "Oops", "You must confirm that the visitor is authorized to enter")
            return

        for field, input_widget in self.fields_inputs.items():
            if not input_widget.text():
                QMessageBox.warning(self, "Input Error", f"{field} cannot be empty!")
                return

        meta = {}

        for field, input_widget in self.fields_inputs.items():
            meta[field] = input_widget.text()

        visitor_data = {
            "name": name,
            "visitorId": visitor_id,
            "meta": meta
        }

        json_str = json.dumps(visitor_data, ensure_ascii=False, indent=4)
        
        self.submitted_data = json_str

        QMessageBox.information(self, "Success", "Form submitted successfully!")
        self.accept()

    def get_submitted_json(self):
        return self.submitted_data