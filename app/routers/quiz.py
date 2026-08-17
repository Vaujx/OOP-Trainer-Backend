from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..content import TOPICS_BY_ID
from .. import models, schemas
from .levels import get_learner_id

router = APIRouter(tags=["quiz"])


def _get_or_create_progress(db: Session, learner_id: str, topic_id: str) -> models.Progress:
    row = (
        db.query(models.Progress)
        .filter(models.Progress.learner_id == learner_id, models.Progress.topic_id == topic_id)
        .first()
    )
    if not row:
        row = models.Progress(learner_id=learner_id, topic_id=topic_id)
        db.add(row)
        db.flush()
    return row


@router.post("/topics/{topic_id}/quiz/submit", response_model=schemas.QuizResultOut)
def submit_quiz(
    topic_id: str,
    payload: schemas.QuizSubmitIn,
    db: Session = Depends(get_db),
    learner_id: str = Depends(get_learner_id),
):
    entry = TOPICS_BY_ID.get(topic_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Topic not found")
    quiz = entry["topic"]["quiz"]

    results = []
    score = 0
    for q in quiz:
        chosen = payload.answers.get(q["id"])
        correct = chosen == q["correct"]
        if correct:
            score += 1
        results.append(
            {
                "question_id": q["id"],
                "correct": correct,
                "correct_option": q["correct"],
                "explanation": q["explanation"],
            }
        )

    total = len(quiz)
    passed = total > 0 and score == total

    row = _get_or_create_progress(db, learner_id, topic_id)
    row.quiz_attempts = (row.quiz_attempts or 0) + 1
    row.quiz_best_score = max(row.quiz_best_score or 0, score)
    if passed:
        row.quiz_completed = True
    db.commit()

    return schemas.QuizResultOut(score=score, total=total, passed=passed, results=results)
