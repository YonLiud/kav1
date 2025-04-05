import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from qasync import QEventLoop, asyncClose, asyncSlot
import asyncio

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("KAV1")
    app.setOrganizationName("yxnliu")
    app.setOrganizationDomain("yxnliu.net")

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Create main window
    main_window = MainWindow()
    main_window.show()

    # Start the event loop
    with loop:
        sys.exit(loop.run_forever())

if __name__ == "__main__":
    main()  