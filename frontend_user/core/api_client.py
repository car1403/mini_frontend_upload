"""모든 메뉴 API에서 공통으로 사용하는 HTTP 요청 기능."""

import os
from typing import Any

import httpx


BACKEND_URL = "http://127.0.0.1:8000"
# BACKEND_URL = "https://mini-frontend-02-mock-m4wy.onrender.com"
REQUEST_TIMEOUT = 15.0


class BackendAPIError(Exception):
    """백엔드 연결 또는 API 응답 처리 중 발생한 오류입니다."""


def request(method: str, 
            path: str, 
            json: dict[str, Any] | None = None,
            data: dict[str, Any] | None = None,
            files: dict[str, Any] | None = None, 
            params: dict[str, Any] | None = None,
            ):
    try:
        response = httpx.request(
            method,
            f"{BACKEND_URL}{path}",
            json=json,
            data=data,
            files=files,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as error:
        raise BackendAPIError("백엔드 응답 시간이 초과되었습니다.") from error
    except httpx.RequestError as error:
        raise BackendAPIError(
            "백엔드 서버에 연결할 수 없습니다. 서버 실행 상태를 확인해 주세요."
        ) from error

    if response.status_code  == 401:
        raise BackendAPIError(
            "로그인 아이디 또는 패스워드 문제"
        )
    if response.status_code  == 404:
        raise BackendAPIError(
            "존재하지 않습니다."
        )
    if response.status_code  == 409:
        raise BackendAPIError(
            "ID가 사용 중 입니다."
        )
   
    if response.is_error:
        try:
            error_payload = response.json()
            detail = error_payload.get("detail", error_payload)
        except ValueError:
            detail = response.text or "알 수 없는 오류"
        raise BackendAPIError(f"요청에 실패했습니다 ({response.status_code}): {detail}")

    try:
        payload = response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error
   
    return payload
