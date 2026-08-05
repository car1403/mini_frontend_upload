from datetime import date
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

def search_item( 
    name: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_price: int | None = None,
    max_price: int | None = None,):

    param_data = {
        "name":name,
        "start_date":start_date,
        "end_date":end_date,
        "min_price":min_price,
        "max_price":max_price
    }
    param_data = {
        key: value
        for key, value in param_data.items()
        if value is not None
    }
    # Query Parameters를 이용한 검색 기능 구현
    # ?aa=bb&cc=dd
    return request("GET", f"/item/search", params= param_data)
