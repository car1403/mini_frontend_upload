from core.api_client import request

def login_process(id:str, pwd:str):
    """  로그인 진행 ID와 PWD 입력 하면 사용자 정보 리턴"""
    return request("POST", f"/auth/signin", json={"id":id, "pwd":pwd})

def logout_process(id:str):
    return request("GET", f"/auth/signout/{id}")

def mypage_process(id:str):
    return request("GET", f"/auth/mypage/{id}")

def register_process(auth:dict):
    return request("POST", f"/auth/create", json=auth)

def update_process(auth:dict):
    return request("PUT", f"/auth/update", json=auth)