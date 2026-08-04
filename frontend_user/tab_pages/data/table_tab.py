import pandas as pd
import streamlit as st

from core.auth import is_logged_in


def show_table() -> None:
    st.subheader("테이블")

    if not is_logged_in():
        st.warning("로그인이 필요한 화면입니다.")
        return

    data = {
        "과정": ["Python", "Streamlit", "FastAPI"],
        "시간": [24, 16, 32],
        "난이도": ["기초", "기초", "중급"],
    }
    dataframe = pd.DataFrame(data)

    st.write("데이터프레임")
    st.dataframe(dataframe, use_container_width=True)

    st.write("테이블")
    st.table(dataframe)
