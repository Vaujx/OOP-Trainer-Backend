import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models  # noqa: F401 - ensures models are registered before create_all
from .routers import levels, quiz, challenge, interview

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OOP Dojo API", version="1.0.0")

# Set FRONTEND_ORIGIN on Render to your Vercel URL (e.g. https://oop-dojo.vercel.app).
# Comma-separate multiple origins if needed. Falls back to "*" for local dev.
_origins_env = os.getenv("FRONTEND_ORIGIN", "*")
origins = ["*"] if _origins_env == "*" else [o.strip() for o in _origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(levels.router)
app.include_router(quiz.router)
app.include_router(challenge.router)
app.include_router(interview.router)


@app.get("/")
def health():
    return {"status": "ok", "service": "oop-dojo-api"}
