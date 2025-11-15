from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env if it exists.

class Config(object):
    """Base Config Object"""
    DEBUG = False
    MONGO_URI = os.environ.get("MONGO")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")