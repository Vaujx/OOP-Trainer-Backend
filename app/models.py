from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from .database import Base


class Progress(Base):
    """One row per (learner, topic). No login system - the frontend generates
    a random learner id on first visit and stores it in localStorage, sent
    back as the X-Learner-Id header. That's enough to keep progress separate
    per person/browser without building real auth for a personal trainer."""

    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("learner_id", "topic_id", name="uq_learner_topic"),)

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(String, index=True, nullable=False)
    topic_id = Column(String, index=True, nullable=False)

    quiz_completed = Column(Boolean, default=False)
    quiz_best_score = Column(Integer, default=0)
    quiz_attempts = Column(Integer, default=0)

    challenge_completed = Column(Boolean, default=False)
    challenge_attempts = Column(Integer, default=0)
    best_code = Column(Text, default="")

    interview_reviewed_count = Column(Integer, default=0)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
