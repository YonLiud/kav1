import sys
from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow

sys.argv += ['-platform', 'windows:darkmode=2']

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()