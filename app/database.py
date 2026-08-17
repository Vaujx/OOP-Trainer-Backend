import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# On Render, set DATABASE_URL to a Postgres connection string (Render offers a
# free Postgres instance) so progress survives deploys/restarts. Locally it
# falls back to a SQLite file so you can run everything with zero setup.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./oop_trainer.db")

# Render's Postgres URLs sometimes start with "postgres://" which SQLAlchemy
# 2.x no longer accepts - normalize to "postgresql://".
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
