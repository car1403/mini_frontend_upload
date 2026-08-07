from datetime import date
from typing import Any

from core.api_client import request


def send_message(user_id: str,prompt: str,):
    return request(
        "POST",
        "/chat/gemini",
        json={"user_id": user_id, "prompt": prompt},
    )

