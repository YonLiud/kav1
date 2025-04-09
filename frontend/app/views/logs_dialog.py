from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QLabel, QHBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtCore import QByteArray

from .warning_dialog import show_warning
from app.core.api_client import ApiClient
from app.core.settings import Settings

class LogsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visitor Logs")
        self.api_client = ApiClient.get_instance()
        self.pending_downloads = {}  # {url: {type: "single"/"all", default_name: str}}
        
        # Setup UI
        self._setup_ui()
        
        # Connect only the response_received signal
        self.api_client.response_received.connect(self._handle_response)
        
        # Initial load
        self._load_logs()
    
    def _setup_ui(self):
        """Initialize all UI components"""
        self.layout = QVBoxLayout(self)
        
        # Log list
        self.layout.addWidget(QLabel("Available Log Files:"))
        self.log_list = QListWidget()
        self.layout.addWidget(self.log_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self._load_logs)
        btn_layout.addWidget(self.btn_refresh)
        
        self.btn_download = QPushButton("Download Selected")
        self.btn_download.clicked.connect(self._start_single_download)
        btn_layout.addWidget(self.btn_download)
        
        self.btn_download_all = QPushButton("Download All (ZIP)")
        self.btn_download_all.clicked.connect(self._start_bulk_download)
        btn_layout.addWidget(self.btn_download_all)
        
        self.layout.addLayout(btn_layout)
    
    def _load_logs(self):
        """Request log list from API"""
        self.log_list.clear()
        self.api_client.list_log_files()
    
    def _handle_response(self, response):
        """
        Handle different types of API responses:
        - dict: JSON responses (log list)
        - QNetworkReply: File downloads
        """
        if isinstance(response, dict):
            if "logs" in response:  # Log list response
                self.log_list.addItems(response["logs"])
            elif "error" in response:  # Handle JSON errors if your API returns them
                show_warning("Error", response["error"])
        
        elif isinstance(response, QNetworkReply):  # File download
            self._process_download(response)
    
    def _start_single_download(self):
        """Initiate download of selected log file"""
        selected = self.log_list.currentItem()
        if not selected:
            show_warning("Error", "No log file selected")
            return
            
        log_name = selected.text()
        url = Settings.get_http_url(f"/visitors/logs/download/{log_name}")
        
        # Track this download
        self.pending_downloads[url] = {
            "type": "single",
            "default_name": log_name
        }
        
        self.api_client.download_log(log_name)
    
    def _start_bulk_download(self):
        """Initiate download of all logs as ZIP"""
        url = Settings.get_http_url("/visitors/logs/download/all")
        
        # Track this download
        self.pending_downloads[url] = {
            "type": "all",
            "default_name": "visitor_logs.zip"
        }
        
        self.api_client.download_all_logs()
    
    def _process_download(self, reply: QNetworkReply):
        """Handle completed file download"""
        url = reply.url().toString()
        download_info = self.pending_downloads.get(url)
        
        if not download_info:
            reply.deleteLater()
            return
            
        try:
            # Check for errors
            if reply.error() != QNetworkReply.NoError:
                show_warning("Download Failed", reply.errorString())
                return
                
            # Get file data (convert QByteArray to bytes)
            file_data = reply.readAll().data()
            
            # Set up file dialog
            file_filter = ("Log Files (*.log);;All Files (*)" 
                          if download_info["type"] == "single" 
                          else "ZIP Archives (*.zip);;All Files (*)")
            
            # Show save dialog
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                download_info["default_name"],
                file_filter
            )
            
            if save_path:
                # Write file to disk
                with open(save_path, "wb") as f:
                    f.write(file_data)
                
                QMessageBox.information(
                    self,
                    "Download Complete",
                    f"File saved to:\n{save_path}"
                )
        
        except Exception as e:
            show_warning("Save Failed", str(e))
        
        finally:
            # Clean up
            if url in self.pending_downloads:
                del self.pending_downloads[url]
            reply.deleteLater()