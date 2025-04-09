from PySide6.QtWidgets import QMessageBox

def show_warning(
    message: str,
    detail: str = "Please ensure your network is active and the server is accessible.",
    icon=QMessageBox.Warning,
    parent=None
):
    """Display a standardized warning dialog with improved formatting.
    
    Args:
        message: Short summary of the warning (used as window title)
        detail: Detailed explanation (auto-formatted with line breaks)
        icon: Qt icon to display (defaults to Warning)
        parent: Parent widget for proper dialog positioning
    """
    msg = QMessageBox(parent)
    msg.setIcon(icon)
    msg.setWindowTitle(message)
    
    # Auto-format details with proper line wrapping
    formatted_detail = "\n".join([
        f"{line.strip()}" if not line.startswith(" ") else line
        for line in detail.split("\n")
    ])
    
    msg.setText(formatted_detail)
    msg.setStandardButtons(QMessageBox.Ok)
    
    # Set reasonable dialog size
    msg.setMinimumWidth(400)
    msg.exec()