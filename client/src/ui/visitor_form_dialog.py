from PySide6.QtWidgets import QDialog, QLineEdit, QFormLayout, QVBoxLayout, QPushButton, QMessageBox, QWidget, QCheckBox, QScrollArea
from PySide6.QtCore import Qt

class VisitorFormDialog(QDialog):
    def __init__(self, fields):
        super().__init__()

        self.setWindowTitle("Visitor Form")
        self.setMinimumSize(800, 500)

        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Visitor's Name")
        self.layout.addRow("Name:", self.name_input)

        self.fields_inputs = {}
        for field in fields:
            field_input = QLineEdit()
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

    def on_submit_clicked(self):
        name = self.name_input.text()
        security_agreed = self.security_checkbox.isChecked()

        if not name:
            QMessageBox.warning(self, "Input Error", "Name cannot be empty!")
            return
        if not security_agreed:
            QMessageBox.warning(self, "Oops", "You must confirm that the visitor is authorized to enter")
            return

        for field, input_widget in self.fields_inputs.items():
            if not input_widget.text():
                QMessageBox.warning(self, "Input Error", f"{field} cannot be empty!")
                return

        data = {"Name": name, "Security Agreement": "Agreed" if security_agreed else "Not Agreed"}
        for field, input_widget in self.fields_inputs.items():
            data[field] = input_widget.text()

        print("Form Data:")
        for key, value in data.items():
            print(f"{key}: {value}")

        QMessageBox.information(self, "Success", "Form submitted successfully!")
        self.accept()

from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        fields = ["Email", "Phone Number", "Purpose of Visit", "Address", "Company Name", "Date of Visit"]

        dialog = VisitorFormDialog(fields)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
