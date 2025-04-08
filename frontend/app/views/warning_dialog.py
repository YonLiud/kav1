from PySide6.QtWidgets import QMessageBox

def show_warning(message: str, detail: str = "Please ensure your network is active and the server is accessible.", icon = QMessageBox.Warning):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setWindowTitle(message)
    msg.setText(detail)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()
