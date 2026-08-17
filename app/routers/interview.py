from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..content import TOPICS_BY_ID
from .. import schemas
from .levels import get_learner_id
from .quiz import _get_or_create_progress

router = APIRouter(tags=["interview"])


@router.post("/topics/{topic_id}/interview/review", response_model=schemas.TopicSummaryOut)
def mark_reviewed(
    topic_id: str,
    payload: schemas.InterviewReviewIn,
    db: Session = Depends(get_db),
    learner_id: str = Depends(get_learner_id),
):
    """Called once the learner reveals/self-grades an interview prompt's model
    answer. We don't try to auto-grade free-form spoken/written answers - the
    learner marks it reviewed after comparing their own answer."""
    entry = TOPICS_BY_ID.get(topic_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic = entry["topic"]
    total = len(topic["interview"])

    row = _get_or_create_progress(db, learner_id, topic_id)
    row.interview_reviewed_count = min(total, (row.interview_reviewed_count or 0) + 1)
    db.commit()

    from . import levels as levels_router
    return levels_router._topic_summary(topic, row)
