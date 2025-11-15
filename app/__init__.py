from flask import Flask
from .config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": ["http://localhost:5173"]}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

from app import views