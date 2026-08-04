# item_router.py

from typing import Annotated

from fastapi import (
    APIRouter, HTTPException, UploadFile, File, Form
)
from app.schemas.item_schema import ItemCreate
from app.services.image_service import save_image
from app.services.item_service import (
    item_create,
)
from app.core.api_response import ApiResponse

item_router = APIRouter(tags=["Item"])

# 200: 정상 - 정상 실행 되면 자동 전송
# 400: 잘못된 요청
# 401: 로그인 필요
# 403: 권한 없음
# 404: 데이터 없음
# 409: 중복 데이터
# 422: 입력값 검증 실패
# 500: 서버 또는 DB 처리 실패

# 1. create
@item_router.post("/item/create")
async def create(
    name: Annotated[str, Form(min_length=1, max_length=50)],
    price: Annotated[int, Form(ge=1)],
    desc: Annotated[str, Form(min_length=1, max_length=200)],
    image: Annotated[UploadFile | None, File()] = None,
) -> ApiResponse:

    image_url, image_filename = await save_image(image)
    item = ItemCreate(
        name=name,
        price=price,
        desc=desc,
        image_url=image_url,
        image_filename=image_filename,
    )
    # name, price, desc
    created_product = item_create(item)
    if created_product is None:
        raise HTTPException(
            status_code=500,
            detail="상품 등록에 실패했습니다.",
        )
    response = ApiResponse(
        success = True,
        message="상품이 등록되었습니다.",
        data = created_product
    )
    return response
