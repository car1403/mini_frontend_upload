# item_router.py

from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter, HTTPException, UploadFile, File, Form
)
from app.schemas.item_schema import ItemCreate
from app.services.image_service import delete_image, save_image
from app.services.item_service import (
    item_create,
    item_get,
    item_get_all,
    item_update,
    item_delete,
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


@item_router.get("/item/getall")
def get_all() -> ApiResponse:
    items = item_get_all()
    return ApiResponse(
        success=True,
        message="상품 목록을 조회했습니다.",
        data=items,
    )


@item_router.get("/item/get/{item_id}")
def get(item_id: int) -> ApiResponse:
    item = item_get(item_id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {item_id}를 찾을 수 없습니다.",
        )
    return ApiResponse(
        success=True,
        message="상품을 조회했습니다.",
        data=item,
    )


@item_router.put("/item/update/{item_id}")
async def update(
    item_id: int,
    name: Annotated[str, Form(min_length=1, max_length=50)],
    price: Annotated[int, Form(ge=1)],
    desc: Annotated[str, Form(min_length=1, max_length=200)],
    image: Annotated[UploadFile | None, File()] = None,
) -> ApiResponse:
    current_item = item_get(item_id)
    if current_item is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    image_url = current_item.image_url
    image_filename = current_item.image_filename

    if image is not None and image.filename:
        new_image_url, new_image_filename = await save_image(image)
        image_url = new_image_url
        image_filename = new_image_filename

    updated_item = item_update(
        item_id=item_id,
        name=name,
        price=price,
        description=desc,
        image_url=image_url,
        image_filename=image_filename,
    )
    if updated_item is None:
        raise HTTPException(status_code=500, detail="상품 수정에 실패했습니다.")

    if image_filename != current_item.image_filename:
        delete_image(current_item.image_filename)

    return ApiResponse(
        success=True,
        message="상품을 수정했습니다.",
        data=updated_item,
    )


@item_router.delete("/item/delete/{item_id}")
def delete(item_id: int) -> ApiResponse:
    current_item = item_get(item_id)
    if current_item is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    deleted_item = item_delete(item_id)
    if deleted_item is None:
        raise HTTPException(status_code=500, detail="상품 삭제에 실패했습니다.")

    delete_image(current_item.image_filename)
    return ApiResponse(
        success=True,
        message="상품을 삭제했습니다.",
        data=deleted_item,
    )

# Query Parameters를 이용한 검색 기능 구현
@item_router.get("/item/search")
def search(
    name: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    ) -> ApiResponse:
    ""
    # 서비스 호출 후 결과를 받아서 리턴