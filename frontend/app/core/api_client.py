from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QJsonDocument
import json
from .settings import Settings

class ApiClient(QObject):
    response_received = Signal(object)
    error_occurred = Signal(str)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ApiClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """Method to get the singleton instance of ApiClient."""
        if cls._instance is None:
            cls._instance = ApiClient()
        return cls._instance


    def __init__(self):
        super().__init__()
        if not hasattr(self, 'manager'):
            self.manager = QNetworkAccessManager()
            self.manager.finished.connect(self._handle_response)

    def get_visitors(self):
        url = Settings.get_http_url("/visitors")
        self._send_request(url, "GET")

    def get_visitors_inside(self):
        url = Settings.get_http_url("/visitors/inside")
        self._send_request(url, "GET")

    def get_visitor_by_id(self, query: str):
        url = Settings.get_http_url(f"/visitors/{query}")
        self._send_request(url, "GET")

    def search_visitors(self, query: str):
        url = Settings.get_http_url(f"/visitors/search?search_query={query}")
        self._send_request(url, "GET")

    def update_visitor_status(self, visitor_id: str, is_inside: bool):
        url = Settings.get_http_url(f"/visitors/{visitor_id}/status?is_inside={is_inside}")
        self._send_request(url, "POST")

    def _send_request(self, url: str, method: str, data: dict = None):
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        
        if method == "GET":
            self.manager.get(request)
        elif method == "POST":
            json_data = QJsonDocument.fromVariant(data).toJson()
            self.manager.post(request, json_data)

    @Slot(object)
    def _handle_response(self, reply):
        try:
            raw_data = reply.readAll()
            print(raw_data)

            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            print(f"Status Code: {status_code}")

            if status_code != 200:
                self.error_occurred.emit(f"HTTP Error: {status_code}")
            else:
                decoded_data = raw_data.data().decode('utf-8')
                data = json.loads(decoded_data)
                print("Parsed data before emitting:", data)
                self.response_received.emit(data)
        finally:
            reply.deleteLater()
