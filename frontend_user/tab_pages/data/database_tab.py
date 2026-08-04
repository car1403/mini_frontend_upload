import streamlit as st

from core.auth import is_logged_in


def show_database() -> None:
    st.subheader("DB 조회")

    if not is_logged_in():
        st.warning("로그인이 필요한 화면입니다.")
        return

    st.info("데이터베이스 조회 결과가 표시될 자리입니다.")
