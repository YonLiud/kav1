from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QJsonDocument
import json

from .settings import Settings
from app.utils.log import Log

class ApiClient(QObject):
    response_received = Signal(object)
    error_occurred = Signal(str)

    logger = Log()

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
            ApiClient.logger.write_to_log("API Client initialized")

    def get_visitors(self):
        url = Settings.get_http_url("/visitors")
        ApiClient.logger.write_to_log(f"Sending GET request to {url}")
        self._send_request(url, "GET")

    def get_visitors_inside(self):
        url = Settings.get_http_url("/visitors/inside")
        ApiClient.logger.write_to_log(f"Sending GET request to {url}")
        self._send_request(url, "GET")

    def get_visitor_by_id(self, query: str):
        url = Settings.get_http_url(f"/visitors/{query}")
        ApiClient.logger.write_to_log(f"Sending GET request to {url} with query: {query}")
        self._send_request(url, "GET")

    def search_visitors(self, query: str):
        url = Settings.get_http_url(f"/visitors/search?search_query={query}")
        ApiClient.logger.write_to_log(f"Sending GET request to {url} with search query: {query}")
        self._send_request(url, "GET")

    def update_visitor_status(self, visitor_id: str, is_inside: bool):
        url = Settings.get_http_url(f"/visitors/{visitor_id}/status?is_inside={is_inside}")
        ApiClient.logger.write_to_log(f"Sending POST request to {url} with visitor ID: {visitor_id} and status: {is_inside}")
        self._send_request(url, "POST")

    def create_visitor(self, visitor: dict):
        url = Settings.get_http_url(f"/visitor")
        ApiClient.logger.write_to_log(f"Sending POST request to {url} with visitor data: {visitor}")
        self._send_request(url, "POST", visitor)

    def _send_request(self, url: str, method: str, data: dict = None):
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        if method == "GET":
            ApiClient.logger.write_to_log(f"Sending GET request to {url}")
            self.manager.get(request)
        elif method == "POST":
            json_data = QJsonDocument.fromVariant(data).toJson()
            ApiClient.logger.write_to_log(f"Sending POST request to {url} with data: {json.dumps(data)}")
            self.manager.post(request, json_data)

    @Slot(object)
    def _handle_response(self, reply):
        try:
            raw_data = reply.readAll()
            ApiClient.logger.write_to_log(f"Response received: {raw_data}")

            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            ApiClient.logger.write_to_log(f"HTTP Status Code: {status_code}")

            if status_code != 200:
                ApiClient.logger.write_to_log(f"Error occurred: HTTP {status_code}")
                self.error_occurred.emit(f"HTTP Error: {status_code}")
            else:
                decoded_data = raw_data.data().decode('utf-8')
                data = json.loads(decoded_data)
                self.response_received.emit(data)
        finally:
            reply.deleteLater()
            ApiClient.logger.write_to_log("Response handling complete, cleaned up.")
