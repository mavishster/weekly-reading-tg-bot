from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str


def get_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise ValueError(
            "BOT_TOKEN is not configured in the .env file."
        )

    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./weekly_reading.db",
    )

    return Settings(
        bot_token=bot_token,
        database_url=database_url,
    )