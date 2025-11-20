import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from server.config import Config
from server.models import init_db
from server.routers import auth as auth_router
from server.routers import entries as entries_router

app = FastAPI()

# CORS - allow the client (Vite) origin used previously
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Session middleware (uses the SECRET_KEY from config)
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)


@app.on_event("startup")
def on_startup():
	# connect to MongoDB if MONGO_URI provided
	init_db(Config.MONGO_URI)


# Include routers
app.include_router(auth_router.router)
app.include_router(entries_router.router)


if __name__ == "__main__":
	# run with: python server/main.py (this will start uvicorn)
	import uvicorn

	uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
