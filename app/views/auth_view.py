from flask import Blueprint, request, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from functools import wraps
import os

auth_bp = Blueprint("auth_bp", __name__, url_prefix=os.getenv("API_PREFIX"))

@auth_bp.route(os.getenv("SIGN_UP"), methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role") # "caretaker" or "med_professional"

    if User.objects(email=email).first():
        return jsonify({ "error": "Email already exists" }), 400
    
    hashed_pw = generate_password_hash(password)

    if role == "med_professional" or role == "caretaker":
        professional = User(
            email=email,
            password=hashed_pw,
            role=role
        ).save()

    return jsonify({ 
        "message": "User created", 
        "user_id": str(professional.id) 
        }), 201

@auth_bp.route(os.getenv("LOG_IN"), methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.objects(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({ "error": "Wrong credentials" }), 401
    
    session["user_id"] = str(user.id)
    session['role'] = user.role

    return jsonify({
        "message": "Logged in",
        "role": user.role,
        "user_id": session["user_id"]
    }), 200

@auth_bp.route(os.getenv("LOGOUT"), methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "messgae": "Logged out successfully"
    }), 200

@auth_bp(os.getenv("GET_SESH"), methods=["GET"])
def get_session():
    if "user_id" in session:
        return jsonify({
            "error": "No active session"
        }), 401
    
    return jsonify({
        "user_id": session.get("user_id"),
        "role": session.get()
    }), 200

# protect routes
def login_req(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "error": "Unauthorized"
            }), 401
        
        g.user_id = session["user_id"]
        g.role = session["role"]
        return f(*args, **kwargs)
    return decorated
