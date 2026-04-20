from sqlalchemy import text

from app.extensions import db


def ping_database() -> None:
    db.session.execute(text("SELECT 1"))