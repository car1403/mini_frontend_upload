import streamlit as st

from clients.item_client import create_item
from core.api_client import BackendAPIError


st.title("상품등록 페이지")

with st.form("create_item_form", clear_on_submit=True):
    name = st.text_input("상품명")
    price = st.number_input("가격", min_value=1, step=1000)
    desc = st.text_area("상품 설명")
    image = st.file_uploader(
        "이미지",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
    )
    submit_button = st.form_submit_button("등록")

if submit_button:
    if not name.strip() or not desc.strip():
        st.error("상품명과 상품 설명을 입력해 주세요.")
    else:
        try:
            result = create_item(
                name=name.strip(),
                price=int(price),
                desc=desc.strip(),
                image=image,
            )
            if result.get("success"):
                st.success(f"상품 '{name}'이(가) 등록되었습니다.")
            else:
                st.error(result.get("message", "상품 등록에 실패했습니다."))
        except BackendAPIError as error:
            st.error(str(error))
