from __future__ import annotations

from flask import Blueprint, current_app, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest, Unauthorized

from app.extensions import db
from app.models.user import User
from app.utils.response import success_response


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config.get("AUTH_TOKEN_SALT", "formatbridge-auth-token"),
    )


def generate_auth_token(user: User) -> str:
    serializer = get_serializer()
    return serializer.dumps({"user_id": user.id, "email": user.email})


def get_token_max_age_seconds() -> int:
    hours = int(current_app.config.get("AUTH_TOKEN_EXPIRY_HOURS", 72))
    return hours * 3600


def decode_auth_token(token: str) -> dict:
    serializer = get_serializer()

    try:
        return serializer.loads(token, max_age=get_token_max_age_seconds())
    except SignatureExpired as exc:
        raise Unauthorized("Authentication token has expired.") from exc
    except BadSignature as exc:
        raise Unauthorized("Authentication token is invalid.") from exc


def get_bearer_token_from_request() -> str | None:
    auth_header = request.headers.get("Authorization", "").strip()
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.replace("Bearer ", "", 1).strip()


def get_current_user_from_request(required: bool = True) -> User | None:
    token = get_bearer_token_from_request()

    if not token:
        if required:
            raise Unauthorized("Authentication is required.")
        return None

    payload = decode_auth_token(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise Unauthorized("Authentication token payload is invalid.")

    user = db.session.get(User, user_id)
    if not user or not user.is_active:
        raise Unauthorized("Authenticated user was not found or is inactive.")

    return user


@auth_bp.post("/signup")
def signup():
    payload = request.get_json(silent=True) or {}

    full_name = (payload.get("full_name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not full_name:
        raise BadRequest("full_name is required.")
    if not email:
        raise BadRequest("email is required.")
    if "@" not in email:
        raise BadRequest("email must be valid.")
    if len(password) < 8:
        raise BadRequest("password must be at least 8 characters long.")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise BadRequest("An account with that email already exists.")

    user = User(full_name=full_name, email=email, is_active=True)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = generate_auth_token(user)

    return success_response(
        "Account created successfully.",
        data={
            "user": user.to_dict(),
            "token": token,
        },
        status_code=201,
    )


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email:
        raise BadRequest("email is required.")
    if not password:
        raise BadRequest("password is required.")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        raise Unauthorized("Invalid email or password.")

    if not user.is_active:
        raise Unauthorized("This account is inactive.")

    token = generate_auth_token(user)

    return success_response(
        "Login successful.",
        data={
            "user": user.to_dict(),
            "token": token,
        },
        status_code=200,
    )


@auth_bp.get("/me")
def me():
    user = get_current_user_from_request(required=True)

    return success_response(
        "Authenticated user fetched successfully.",
        data={"user": user.to_dict()},
        status_code=200,
    )