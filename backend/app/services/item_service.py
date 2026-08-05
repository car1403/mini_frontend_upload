# item_service.py
from app.schemas.item_schema import ItemCreate, ItemPublic
from app.core.supabase_config import get_supabase
from zoneinfo import ZoneInfo
from datetime import date, datetime

# 1. 입력
def item_create(item: ItemCreate) -> ItemPublic | None:
    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    result = (
        supabase.table("items")
         .insert(
            {
                "name": item.name,
                "price": item.price,
                "description": item.desc,
                "image_url": item.image_url,
                "image_filename": item.image_filename,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }
        )
        .execute()
    )
    if not result.data:
        return None
    return ItemPublic.model_validate(result.data[0])


def item_get_all() -> list[ItemPublic]:
    supabase = get_supabase()
    result = (
        supabase.table("items")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return [ItemPublic.model_validate(item) for item in result.data]


def item_get(item_id: int) -> ItemPublic | None:
    supabase = get_supabase()
    result = (
        supabase.table("items")
        .select("*")
        .eq("id", item_id)
        .execute()
    )
    if not result.data:
        return None
    return ItemPublic.model_validate(result.data[0])


def item_update(
    item_id: int,
    name: str,
    price: int,
    description: str,
    image_url: str | None,
    image_filename: str | None,
) -> ItemPublic | None:
    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    result = (
        supabase.table("items")
        .update(
            {
                "name": name,
                "price": price,
                "description": description,
                "image_url": image_url,
                "image_filename": image_filename,
                "updated_at": now.isoformat(),
            }
        )
        .eq("id", item_id)
        .execute()
    )
    if not result.data:
        return None
    return ItemPublic.model_validate(result.data[0])


def item_delete(item_id: int) -> ItemPublic | None:
    supabase = get_supabase()
    result = (
        supabase.table("items")
        .delete()
        .eq("id", item_id)
        .execute()
    )
    if not result.data:
        return None
    return ItemPublic.model_validate(result.data[0])

def item_search(
    name: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    ):
    ""
    supabase = get_supabase()
    query = supabase.table("items").select("*")

    if name:
        query = query.ilike("name", f"%{name}%") 

    if min_price is not None:
        query = query.gte("price", min_price)

    if max_price is not None:
        query = query.lte("price", max_price)

    if start_date:
        query = query.gte("created_at", start_date.isoformat())

    if end_date:
        query = query.lte("created_at", end_date.isoformat())

    result = query.execute()
    return [ItemPublic.model_validate(item) for item in result.data]