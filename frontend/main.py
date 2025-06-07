import sys


from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    with open("style.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
