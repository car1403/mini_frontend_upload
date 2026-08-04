import streamlit as st

from core.auth import is_logged_in
from tab_pages.data.chart_tab import show_chart
from tab_pages.data.database_tab import show_database
from tab_pages.data.log_tab import show_log
from tab_pages.data.table_tab import show_table


if not is_logged_in():
    st.warning("로그인이 필요한 화면입니다.")
else:
    table_tab, chart_tab, log_tab, database_tab = st.tabs(
        ["테이블", "차트", "로그", "DB"]
    )

    with table_tab:
        show_table()

    with chart_tab:
        show_chart()

    with log_tab:
        show_log()

    with database_tab:
        show_database()
