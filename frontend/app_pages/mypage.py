# mypage.py

import streamlit as st
from clients.auth_client import mypage_process, update_process
from core.auth import BackendAPIError, is_logged_in

st.title("My Page")
if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

try:
    with st.spinner("Loading..."):
        get_mypage = mypage_process(st.session_state.login_id)

        with st.form("update_form", clear_on_submit=True):
            update_id = st.text_input(
                "ID",
                value = get_mypage["id"],
                disabled = True,
                placeholder = "수정할 ID를 입력하세요",
            )
            update_pwd = st.text_input(
                "PWD",
                type="password",
                placeholder="비밀번호를 입력하세요",
            )
            update_pwd_com = st.text_input(
                "PWD 확인",
                type="password",
                placeholder="비밀번호를 입력하세요",
            )
            update_name = st.text_input(
                "이름",
                value = get_mypage["name"],
                placeholder="이름을 입력하세요",
            )
            update_submitted = st.form_submit_button(
                "회원정보 수정",
                type="primary",
                use_container_width=True,
            )

        if update_submitted:
            if not update_pwd or not update_pwd_com or not update_name:
                st.warning("PWD, PWD 확인, 이름을 모두 입력해 주세요.")

            if update_pwd != update_pwd_com:
                st.warning("PWD와 PWD 확인이 일치하지 않습니다.")
            else:
                # id, pwd, name을 서버로 전송 후 확인
                ""    
                payload = {
                    "id": update_id,
                    "pwd": update_pwd,
                    "name": update_name
                }
                try:
                    with st.spinner("회원정보 수정 진행 중..."):
                        result = update_process(payload)
                    if result is not None:
                        st.success("회원정보 수정이 완료되었습니다.")
                        st.rerun()
                except BackendAPIError as error:
                    st.error(str(error))
    
except BackendAPIError as error:
    st.error(str(error))

