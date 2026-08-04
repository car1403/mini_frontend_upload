from typing import Any

from core.api_client import request


def create_item(
    name: str,
    price: int,
    desc: str,
    image: Any = None,
):
    files = None
    if image is not None:
        files = {
            "image": (
                image.name,
                image.getvalue(),
                image.type or "application/octet-stream",
            )
        }

    return request(
        "POST",
        "/item/create",
        data={"name": name, "price": str(price), "desc": desc},
        files=files,
    )
