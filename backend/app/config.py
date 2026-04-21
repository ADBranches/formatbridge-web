import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
    
    AUTH_TOKEN_EXPIRY_HOURS = int(os.getenv("AUTH_TOKEN_EXPIRY_HOURS", "72"))
    ALLOW_ANONYMOUS_CONVERSIONS = os.getenv("ALLOW_ANONYMOUS_CONVERSIONS", "true").lower() == "true"
    AUTH_TOKEN_SALT = os.getenv("AUTH_TOKEN_SALT", "formatbridge-auth-token")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config(config_name: str | None = None):
    name = (config_name or os.getenv("FLASK_ENV", "development")).lower()

    mapping = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    return mapping.get(name, DevelopmentConfig)