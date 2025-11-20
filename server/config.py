import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Config for FastAPI server (mirrors Flask config)."""
    DEBUG = False
    MONGO_URI = os.environ.get("MONGO")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    API_PREFIX = os.getenv("API_PREFIX", "/api")
    SIGN_UP = os.getenv("SIGN_UP", "/signup")
    LOG_IN = os.getenv("LOG_IN", "/login")
    LOGOUT = os.getenv("LOGOUT", "/logout")
    GET_SESH = os.getenv("GET_SESH", "/session")
