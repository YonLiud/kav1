from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtWebSockets import QWebSocket


class WebSocketClient(QObject):
    message_received = Signal(str)
    connected = Signal()
    disconnected = Signal()

    def __init__(self):
        super().__init__()
        self.client = QWebSocket()
        self.client.connected.connect(self._on_connected)
        self.client.disconnected.connect(self._on_disconnected)
        self.client.textMessageReceived.connect(self._on_message_received)

    def connect(self, url):
        self.client.open(QUrl(url))

    def send_message(self, message: str):
        if self.client.state() == QWebSocket.State.Connected:
            self.client.sendTextMessage(message)

    def _on_connected(self):
        self.connected.emit()

    def _on_disconnected(self):
        self.disconnected.emit()

    def _on_message_received(self, message: str):
        if message == "sync":
            self.message_received.emit("Server requested sync")
        else:
            self.message_received.emit(f"WS: {message}")
