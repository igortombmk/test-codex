"""Storage abstraction for customer requests.

Supports Google Sheets when configured and CSV fallback for local MVP runs.
"""

import csv
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


logger = logging.getLogger(__name__)

COLUMNS = [
    "created_at",
    "telegram_user_id",
    "username",
    "full_name",
    "request_type",
    "customer_name",
    "contact",
    "stop_address",
    "message",
    "status",
    "responsible",
    "result",
]


class BaseStorage(ABC):
    """Abstract storage interface."""

    @abstractmethod
    def save_request(self, payload: dict) -> bool:
        """Save request payload, return True on success."""


class CSVStorage(BaseStorage):
    """CSV fallback storage for local test mode."""

    def __init__(self, file_path: str = "data/requests.csv"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Create CSV file and headers if not exists."""
        if not self.file_path.exists():
            with self.file_path.open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COLUMNS)

    def save_request(self, payload: dict) -> bool:
        try:
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                payload.get("telegram_user_id", ""),
                payload.get("username", ""),
                payload.get("full_name", ""),
                payload.get("request_type", ""),
                payload.get("customer_name", ""),
                payload.get("contact", ""),
                payload.get("stop_address", ""),
                payload.get("message", ""),
                "new",
                "",
                "",
            ]
            with self.file_path.open("a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
            return True
        except Exception as exc:
            logger.exception("Failed to save request to CSV: %s", exc)
            return False


class GoogleSheetsStorage(BaseStorage):
    """Google Sheets storage backend."""

    def __init__(self, sheet_id: str, service_account_file: str):
        self.sheet_id = sheet_id
        self.service_account_file = service_account_file

    def save_request(self, payload: dict) -> bool:
        try:
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(self.service_account_file, scopes=scopes)
            client = gspread.authorize(creds)
            sheet = client.open_by_key(self.sheet_id).sheet1

            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                payload.get("telegram_user_id", ""),
                payload.get("username", ""),
                payload.get("full_name", ""),
                payload.get("request_type", ""),
                payload.get("customer_name", ""),
                payload.get("contact", ""),
                payload.get("stop_address", ""),
                payload.get("message", ""),
                "new",
                "",
                "",
            ]
            sheet.append_row(row, value_input_option="RAW")
            return True
        except Exception as exc:
            logger.exception("Failed to append request to Google Sheets: %s", exc)
            return False


def get_storage(cfg) -> BaseStorage:
    """Return Google Sheets storage if configured; otherwise CSV fallback."""
    if cfg.google_sheet_id and cfg.google_service_account_file:
        logger.info("Using Google Sheets storage")
        return GoogleSheetsStorage(cfg.google_sheet_id, cfg.google_service_account_file)

    logger.warning("Google Sheets config is incomplete. Falling back to CSV storage: data/requests.csv")
    return CSVStorage("data/requests.csv")
