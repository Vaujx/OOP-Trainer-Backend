from typing import List, Optional
from pydantic import BaseModel


class QuizOptionOut(BaseModel):
    id: str
    text: str


class QuizQuestionOut(BaseModel):
    id: str
    question: str
    options: List[QuizOptionOut]


class ChallengeOut(BaseModel):
    id: str
    prompt: str
    starter_code: str
    example: Optional[str] = None


class InterviewQuestionOut(BaseModel):
    model_config = {"protected_namespaces": ()}

    id: str
    question: str
    hint: Optional[str] = None
    model_answer: Optional[str] = None


class TopicSummaryOut(BaseModel):
    id: str
    title: str
    tagline: str
    quiz_completed: bool = False
    challenge_completed: bool = False
    interview_reviewed_count: int = 0
    interview_total: int = 0


class LevelSummaryOut(BaseModel):
    id: str
    name: str
    belt: str
    color: str
    description: str
    topics: List[TopicSummaryOut]
    topics_completed: int
    topics_total: int


class TopicDetailOut(BaseModel):
    id: str
    level_id: str
    title: str
    tagline: str
    theory: str
    quiz: List[QuizQuestionOut]
    challenge: ChallengeOut
    interview: List[InterviewQuestionOut]
    progress: TopicSummaryOut


class QuizSubmitIn(BaseModel):
    answers: dict  # {question_id: option_id}


class QuizResultOut(BaseModel):
    score: int
    total: int
    passed: bool
    results: List[dict]  # [{question_id, correct: bool, correct_option, explanation}]


class ChallengeSubmitIn(BaseModel):
    code: str


class TestResultOut(BaseModel):
    name: str
    passed: bool
    message: str


class ChallengeResultOut(BaseModel):
    passed: bool
    tests: List[TestResultOut]
    stdout: str
    error: Optional[str] = None


class InterviewReviewIn(BaseModel):
    question_id: str


class ProgressOverviewOut(BaseModel):
    levels: List[LevelSummaryOut]
    overall_percent: float
