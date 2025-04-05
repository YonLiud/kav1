import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from stylesheet import stylesheet

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("KAV1")
    app.setOrganizationName("yxnliu")
    app.setOrganizationDomain("yxnliu.net")

    app.setStyle("WindowsVista")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()