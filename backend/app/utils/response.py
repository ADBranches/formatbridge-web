from __future__ import annotations

from flask import jsonify


def success_response(message: str, data: dict | list | None = None, status_code: int = 200):
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
        "error": None,
    }
    return jsonify(payload), status_code


def error_response(
    message: str,
    status_code: int = 400,
    error_code: str | None = None,
    details: dict | list | None = None,
):
    payload = {
        "success": False,
        "message": message,
        "data": {},
        "error": {
            "code": error_code or "request_error",
            "details": details if details is not None else {},
        },
    }
    return jsonify(payload), status_code