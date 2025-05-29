from datetime import datetime
from typing import Optional
from pathlib import Path


class VisitorLogger:
    _instance = None
    _log_dir = "visitor_logs"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisitorLogger, cls).__new__(cls)
            Path(cls._log_dir).mkdir(exist_ok=True)
        return cls._instance

    def _get_log_file(self):
        """Get today's log file path"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return Path(self._log_dir) / f"visitors_{date_str}.log"

    def log_event(
        self,
        event_type: str,
        visitor_id: str,
        visitor_name: str,
        additional_info: Optional[str] = None,
    ):
        """Log a visitor event

        Args:
            event_type: ENTRY, EXIT, CREATE, DELETE, etc.
            visitor_id: The visitor's unique ID
            visitor_name: The visitor's name
            additional_info: Any additional context
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{event_type},{visitor_id},{visitor_name}"

        if additional_info:
            log_entry += f",{additional_info}"

        log_file = self._get_log_file()
        with open(log_file, "a") as f:
            f.write(log_entry + "\n")

    def get_logs(self, date: Optional[str] = None,
                 max_entries: Optional[int] = None):
        """Get log entries

        Args:
            date: Date in YYYY-MM-DD format (None for today)
            max_entries: Maximum number of entries to return (None for all)
        """
        date_str = date or datetime.now().strftime("%Y-%m-%d")
        log_file = Path(self._log_dir) / f"visitors_{date_str}.log"

        if not log_file.exists():
            return []

        with open(log_file, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if max_entries is not None:
            return lines[-max_entries:]
        return lines

    def get_all_log_files(self):
        """Get list of all available log files"""
        return sorted(Path(self._log_dir).glob("visitors_*.csv"))
