import os

from fastapi import APIRouter, HTTPException, Request, status
from starlette.responses import JSONResponse
from werkzeug.security import check_password_hash, generate_password_hash

from server.config import Config
from server.models import User

api_prefix = Config.API_PREFIX
router = APIRouter(prefix=api_prefix)


@router.post(Config.SIGN_UP)
async def signup(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if User.objects(email=email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = generate_password_hash(password)

    if role in ("med_professional", "caretaker"):
        professional = User(email=email, password=hashed_pw, role=role).save()
    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    return JSONResponse({"message": "User created", "user_id": str(professional.id)}, status_code=201)


@router.post(Config.LOG_IN)
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    user = User.objects(email=email).first()

    if not user or not check_password_hash(user.password, password):
        raise HTTPException(status_code=401, detail="Wrong credentials")

    request.session["user_id"] = str(user.id)
    request.session["role"] = user.role

    return {"message": "Logged in", "role": user.role, "user_id": request.session["user_id"]}


@router.post(Config.LOGOUT)
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}


@router.get(Config.GET_SESH)
async def get_session(request: Request):
    if "user_id" not in request.session:
        raise HTTPException(status_code=401, detail="No active session")

    return {"user_id": request.session.get("user_id"), "role": request.session.get("role")}


def login_required(request: Request):
    if "user_id" not in request.session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": request.session["user_id"], "role": request.session.get("role")}
