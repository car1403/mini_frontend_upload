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


def get_items():
    return request("GET", "/item/getall")


def get_item(item_id: int):
    return request("GET", f"/item/get/{item_id}")


def update_item(
    item_id: int,
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
        "PUT",
        f"/item/update/{item_id}",
        data={"name": name, "price": str(price), "desc": desc},
        files=files,
    )


def delete_item(item_id: int):
    return request("DELETE", f"/item/delete/{item_id}")
