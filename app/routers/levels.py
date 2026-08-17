from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..content import LEVELS, TOPICS_BY_ID
from .. import models
from .. import schemas

router = APIRouter(tags=["levels"])


def get_learner_id(x_learner_id: str = Header(default="anonymous")) -> str:
    return x_learner_id or "anonymous"


def _topic_progress_map(db: Session, learner_id: str):
    rows = db.query(models.Progress).filter(models.Progress.learner_id == learner_id).all()
    return {r.topic_id: r for r in rows}


def _topic_summary(topic: dict, progress_row) -> schemas.TopicSummaryOut:
    return schemas.TopicSummaryOut(
        id=topic["id"],
        title=topic["title"],
        tagline=topic["tagline"],
        quiz_completed=bool(progress_row and progress_row.quiz_completed),
        challenge_completed=bool(progress_row and progress_row.challenge_completed),
        interview_reviewed_count=(progress_row.interview_reviewed_count if progress_row else 0),
        interview_total=len(topic["interview"]),
    )


def _topic_fully_done(summary: schemas.TopicSummaryOut) -> bool:
    return summary.quiz_completed and summary.challenge_completed and summary.interview_reviewed_count >= summary.interview_total


@router.get("/levels", response_model=schemas.ProgressOverviewOut)
def list_levels(db: Session = Depends(get_db), learner_id: str = Depends(get_learner_id)):
    progress_map = _topic_progress_map(db, learner_id)
    level_outs = []
    total_topics = 0
    total_done = 0

    for level in LEVELS:
        topic_summaries = [_topic_summary(t, progress_map.get(t["id"])) for t in level["topics"]]
        done = sum(1 for s in topic_summaries if _topic_fully_done(s))
        total_topics += len(topic_summaries)
        total_done += done
        level_outs.append(
            schemas.LevelSummaryOut(
                id=level["id"],
                name=level["name"],
                belt=level["belt"],
                color=level["color"],
                description=level["description"],
                topics=topic_summaries,
                topics_completed=done,
                topics_total=len(topic_summaries),
            )
        )

    overall = round((total_done / total_topics) * 100, 1) if total_topics else 0.0
    return schemas.ProgressOverviewOut(levels=level_outs, overall_percent=overall)


@router.get("/topics/{topic_id}", response_model=schemas.TopicDetailOut)
def get_topic(topic_id: str, db: Session = Depends(get_db), learner_id: str = Depends(get_learner_id)):
    entry = TOPICS_BY_ID.get(topic_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic, level = entry["topic"], entry["level"]

    row = (
        db.query(models.Progress)
        .filter(models.Progress.learner_id == learner_id, models.Progress.topic_id == topic_id)
        .first()
    )

    quiz_out = [
        schemas.QuizQuestionOut(
            id=q["id"],
            question=q["question"],
            options=[schemas.QuizOptionOut(id=o["id"], text=o["text"]) for o in q["options"]],
        )
        for q in topic["quiz"]
    ]

    challenge_out = schemas.ChallengeOut(
        id=topic["challenge"]["id"],
        prompt=topic["challenge"]["prompt"],
        starter_code=topic["challenge"]["starter_code"],
        example=topic["challenge"].get("example"),
    )

    interview_out = [
        schemas.InterviewQuestionOut(id=q["id"], question=q["question"], hint=q.get("hint"), model_answer=q.get("model_answer"))
        for q in topic["interview"]
    ]

    return schemas.TopicDetailOut(
        id=topic["id"],
        level_id=level["id"],
        title=topic["title"],
        tagline=topic["tagline"],
        theory=topic["theory"],
        quiz=quiz_out,
        challenge=challenge_out,
        interview=interview_out,
        progress=_topic_summary(topic, row),
    )
