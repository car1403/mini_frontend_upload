import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.
from clients.chat_client import send_message  # 백엔드 서버와 통신하기 위해 chat_client.py를 가져옵니다..
from core.auth import is_logged_in  # 로그인 상태를 확인하기 위해 auth.py를 가져옵니다.

if not is_logged_in():
    st.warning("로그인이 필요한 화면입니다.")
else:
    st.title("대화 이력 추가")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

    if "messages" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
        st.session_state.messages = []  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

    for message in st.session_state.messages:  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
        with st.chat_message(message["role"]):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
            st.write(message["content"])  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

    prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

    if prompt:  # 사용자가 채팅 입력창에 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
        with st.spinner("AI가 답변을 작성 중입니다..."):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
            reply = send_message(st.session_state.user_id, prompt)  # 백엔드 또는 AI 서비스가 만든 응답 문자열을 화면 출력용 변수에 저장합니다.
            reply = reply["data"].get("reply", "답변을 받지 못했습니다.")  # 백엔드 또는 AI 서비스가 만든 응답 문자열을 화면 출력용 변수에 저장합니다.
        st.session_state.messages.append({"role": "assistant", "content": reply})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
        st.rerun()  # session_state 변경 사항을 즉시 반영하기 위해 Streamlit 스크립트를 다시 실행합니다.


