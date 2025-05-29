from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QScrollArea, QWidget, QPushButton,
    QLineEdit, QCheckBox, QHBoxLayout)

from app.core.api_client import ApiClient

from app.views.common.warning_dialog import show_warning


class CreateVisitorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Visitor")
        self.setMinimumSize(600, 400)

        self.api_client = ApiClient.get_instance()

        layout = QVBoxLayout(self)

        self.name_field = QLineEdit()
        self.visitorid_field = QLineEdit()

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_field)

        layout.addWidget(QLabel("Visitor ID:"))
        layout.addWidget(self.visitorid_field)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)

        self.scroll_area.setWidget(self.form_widget)
        layout.addWidget(QLabel("properties (key-value pairs):"))
        layout.addWidget(self.scroll_area)

        self.add_field_btn = QPushButton("Add Field")
        self.add_field_btn.clicked.connect(self.add_param_field)
        layout.addWidget(self.add_field_btn)

        self.confirm_checkbox = QCheckBox("I confirm the data is correct")
        layout.addWidget(self.confirm_checkbox)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_btn)

        self.param_fields = []
        self.add_param_field()

        self.api_client.response_received.disconnect()
        self.api_client.response_received.connect(self.on_visitor_found)
        self.api_client.error_occurred.connect(self.on_error)

    def add_param_field(self):
        field_layout = QHBoxLayout()
        key_input = QLineEdit()
        key_input.setPlaceholderText("Key")

        value_input = QLineEdit()
        value_input.setPlaceholderText("Value")

        field_layout.addWidget(key_input)
        field_layout.addWidget(value_input)

        container = QWidget()
        container.setLayout(field_layout)

        self.form_layout.addWidget(container)
        self.param_fields.append((key_input, value_input))

    def submit_data(self):
        if not self.confirm_checkbox.isChecked():
            show_warning(
                "Action Required",
                "Please review and confirm your entries before submitting.\n\n"
                "Double-check:\n"
                "• All required fields are complete\n"
                "• The information is accurate\n"
                "• Any special instructions were followed"
            )
            return

        name = self.name_field.text().strip()
        visitor_id = self.visitorid_field.text().strip()

        if not name or not visitor_id:
            show_warning(
                "Missing Information",
                "Both name and visitor ID are required to continue.\n\n"
                "Please provide:\n"
                "• Full visitor name\n"
                "• Valid visitor ID\n"
                "• Any other required details"
            )
            return

        self.check_visitor_exist(visitor_id)

    def check_visitor_exist(self, visitor_id: str):
        """Check if the visitor already exists using the visitor_id."""
        self.api_client.get_visitor_by_id(visitor_id)

    def on_visitor_found(self, data):
        """
        If visitor is found, check if it's the message 'Visitor not found'.
        If the visitor is found, show a warning.
        If the visitor is not found, proceed to create the visitor.
        """
        if data.get('message') == 'Visitor not found':
            self.create_visitor()
        else:
            show_warning(
                "Duplicate Visitor ID",
                "This ID is already in use. Please try a different ID.\n\n"
                "Tips:\n"
                "• Check for typos in the ID\n"
                "• Search for the existing visitor if needed"
            )

    def on_error(self, error_message):
        """
        Handle error if API call fails.
        """
        show_warning(
            "Operation Failed",
            "An unexpected error occurred:\n\n"
            f"• {error_message}\n\n"
            "Please try again or contact support if the problem persists."
        )

    def create_visitor(self):
        """
        Create a new visitor since the visitor ID was not found.
        """
        name = self.name_field.text().strip()
        visitor_id = self.visitorid_field.text().strip()

        properties = {}
        for key_input, value_input in self.param_fields:
            key = key_input.text().strip()
            val = value_input.text().strip()

            if not key:
                continue

            if val.lower() in ("true", "false"):
                val = val.lower() == "true"
            else:
                try:
                    val = int(val)
                except Exception:
                    pass

            properties[key] = val

        data = {
            "name": name,
            "visitorid": visitor_id,
            "properties": properties
        }

        self.api_client.create_visitor(data)
        self.accept()
