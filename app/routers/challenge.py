from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..content import TOPICS_BY_ID
from .. import models, schemas
from .. import grader
from .levels import get_learner_id
from .quiz import _get_or_create_progress

router = APIRouter(tags=["challenge"])


@router.post("/topics/{topic_id}/challenge/submit", response_model=schemas.ChallengeResultOut)
def submit_challenge(
    topic_id: str,
    payload: schemas.ChallengeSubmitIn,
    db: Session = Depends(get_db),
    learner_id: str = Depends(get_learner_id),
):
    entry = TOPICS_BY_ID.get(topic_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Topic not found")
    challenge = entry["topic"]["challenge"]

    result = grader.run_challenge(payload.code, challenge["tests"])

    row = _get_or_create_progress(db, learner_id, topic_id)
    row.challenge_attempts = (row.challenge_attempts or 0) + 1
    row.best_code = payload.code
    if result["passed"]:
        row.challenge_completed = True
    db.commit()

    return schemas.ChallengeResultOut(
        passed=result["passed"],
        tests=[schemas.TestResultOut(**t) for t in result["tests"]],
        stdout=result["stdout"],
        error=result["error"],
    )
