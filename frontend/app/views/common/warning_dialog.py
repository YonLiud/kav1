from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt


def show_warning(message: str, detail: str, icon=QMessageBox.Warning, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(icon)
    msg.setWindowTitle(message)
    msg.setText(detail)
    msg.setStandardButtons(QMessageBox.Ok)

    msg.setWindowFlags(
        Qt.WindowStaysOnTopHint
        | Qt.Dialog
        | Qt.CustomizeWindowHint
        | Qt.WindowTitleHint
    )
    msg.setWindowModality(Qt.ApplicationModal)

    msg.setModal(True)
    msg.activateWindow()
    msg.raise_()

    msg.setWindowFlag(Qt.WindowCloseButtonHint, False)

    return msg.exec()
