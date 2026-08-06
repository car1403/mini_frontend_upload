
import streamlit as st

from clients.item_client import search_item, get_item, get_items, update_item
from core.api_client import BACKEND_URL, BackendAPIError
from core.date_time import format_created_at



def get_image_url(item: dict) -> str | None:
    image_url = item.get("image_url")
    if image_url and not image_url.startswith(("http://", "https://")):
        return f"{BACKEND_URL}{image_url}"
    return image_url


def show_item_detail(item_id: int) -> None:
    response = get_item(item_id)
    item = response.get("data") or {}

    if st.button("← 상품 목록으로"):
        st.session_state.pop("selected_item_id", None)
        st.rerun()

    if message := st.session_state.pop("item_message", None):
        st.success(message)

    st.title(item.get("name") or "상품 상세조회")
    image_column, info_column = st.columns([2, 3])

    with image_column:
        image_url = get_image_url(item)
        if image_url:
            st.image(image_url, width=300)
        else:
            st.info("이미지 없음")

    with info_column:
        st.subheader(f"{int(item.get('price') or 0):,}원")
        st.write(item.get("description") or "상품 설명이 없습니다.")
        st.caption(f"등록일: {format_created_at(item.get('created_at'))}")

    st.divider()
    


def show_item_list() -> None:
    st.title("상품조회 페이지")

    if message := st.session_state.pop("item_message", None):
        st.success(message)


    with st.form("item-search-form"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            search_name = st.text_input("상품명")
        with col2:
            search_start_date = st.date_input(
                "등록일 시작",
                value=None,
                min_value=None,
                max_value=None,
        )
        with col3:
            search_end_date = st.date_input(
                "등록일 종료",
                value=None,
                min_value=None,
                max_value=None,
            )
        with col4:
            search_min_price = st.number_input(
                "최소 가격",
                min_value=0,
                step=1000,
                value=0,
            )
        with col5:
            search_max_price = st.number_input(
                "최대 가격",
            min_value=0,
            step=1000,
            value=0,
        )
        search_button = st.form_submit_button("검색")

    if search_button:
        response = search_item(
            name=search_name.strip() or None,
            start_date=search_start_date ,
            end_date=search_end_date,
            min_price=search_min_price if search_min_price > 0 else None,
            max_price=search_max_price if search_max_price > 0 else None,
        )
    else:
        response = get_items()






    response = get_items()
    items = response.get("data") or []

    if not items:
        st.info("등록된 상품이 없습니다.")
        return

    st.caption(f"총 {len(items)}개의 상품")

    for item in items:
        with st.container(border=True):
            image_column, info_column, button_column = st.columns([1, 4, 1])

            with image_column:
                image_url = get_image_url(item)
                if image_url:
                    st.image(image_url, width=180)
                else:
                    st.info("이미지 없음")

            with info_column:
                st.subheader(item.get("name") or "이름 없음")
                st.write(f"가격: {int(item.get('price') or 0):,}원")
                st.write(item.get("description") or "상품 설명이 없습니다.")
                st.caption(
                    f"등록일: {format_created_at(item.get('created_at'))}"
                )

            with button_column:
                if st.button("상세보기", key=f"item-detail-{item['id']}"):
                    st.session_state.selected_item_id = item["id"]
                    st.rerun()


try:
    selected_item_id = st.session_state.get("selected_item_id")
    if selected_item_id is None:
        show_item_list()
    else:
        show_item_detail(selected_item_id)
except BackendAPIError as error:
    st.error(str(error))
