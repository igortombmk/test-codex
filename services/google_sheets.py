"""Google Sheets service for saving customer requests."""

import logging
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Simple wrapper around gspread append_row."""

    def __init__(self, sheet_id: str, service_account_file: str):
        self.sheet_id = sheet_id
        self.service_account_file = service_account_file

    def append_request(self, payload: dict) -> bool:
        """Append request row to Google Sheets. Returns True on success."""
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
