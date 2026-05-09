"""Bot configuration module."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Config:
    """Configuration values loaded from environment."""

    bot_token: str
    admin_telegram_id: int
    google_sheet_id: str
    google_service_account_file: str


config = Config(
    bot_token=os.getenv("BOT_TOKEN", ""),
    admin_telegram_id=int(os.getenv("ADMIN_TELEGRAM_ID", "0")),
    google_sheet_id=os.getenv("GOOGLE_SHEET_ID", ""),
    google_service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json"),
)
