import sys
from pathlib import Path

if __name__ == "__main__" and not __package__:
    file = Path(__file__).resolve()
    package_root = file.parents[3]
    sys.path.append(str(package_root))
    __package__ = "frontend.app.views"

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QApplication,
)


class ConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect to Server")

        self.setFixedSize(250, 100)

        self.input = QLineEdit()
        self.input.setPlaceholderText("localhost:3000")

        self.confirm_button = QPushButton("Connect")
        self.confirm_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Server Address:"))
        layout.addWidget(self.input)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

    def get_address(self):
        return self.input.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = ConnectionDialog()
    dialog.show()
    sys.exit(app.exec())
