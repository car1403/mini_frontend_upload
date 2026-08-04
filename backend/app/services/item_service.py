# item_service.py
from app.schemas.product_schema import ItemCreate, ItemPublic, ProductUpdate
from app.core.supabase_client import get_supabase
from zoneinfo import ZoneInfo
from datetime import datetime

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
                "desc": item.desc,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }
        )
        .execute()
    )
    if not result.data:
        return None
    return ItemPublic.model_validate(result.data[0])
