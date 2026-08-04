import streamlit as st


def init_state() -> None:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


def login(user_id: str, password: str) -> bool:
    if user_id == "id01" and password == "pwd01":
        st.session_state.logged_in = True
        return True
    return False


def logout() -> None:
    st.session_state.logged_in = False


def is_logged_in() -> bool:
    return st.session_state.logged_in
