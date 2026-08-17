# OOP Dojo — API

FastAPI backend for the OOP Dojo trainer: serves levels/topics/theory, grades quizzes, and safely executes
your submitted Python code against each challenge's test cases.

## What's in here

```
app/
  main.py         FastAPI app, CORS, router registration
  content.py       ← all training content (levels, theory, quizzes, challenges, interview Q&A)
  grader.py        sandboxed runner that executes learner code against test cases
  models.py        Progress table (SQLAlchemy)
  schemas.py        Pydantic request/response models
  database.py       DB engine/session (SQLite locally, Postgres on Render)
  routers/
    levels.py       GET /levels, GET /topics/{id}
    quiz.py         POST /topics/{id}/quiz/submit
    challenge.py     POST /topics/{id}/challenge/submit
    interview.py      POST /topics/{id}/interview/review
```

There's no login system. The frontend generates a random id per browser (stored in localStorage) and sends
it as the `X-Learner-Id` header, so progress is tracked per-person without needing real auth.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Visit http://127.0.0.1:8000/docs for interactive API docs. A local `oop_trainer.db` SQLite file is created
automatically — delete it any time to reset all progress.

## Deploy to Render

1. Push this repo to GitHub.
2. On Render: **New → Web Service**, connect the repo. Render will pick up `render.yaml` automatically
   (or set manually: build command `pip install -r requirements.txt`, start command
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
3. **Persisting progress**: Render's free web services have an ephemeral filesystem, so SQLite won't
   survive a redeploy. Create a free Render Postgres instance, copy its "External Database URL", and set
   it as the `DATABASE_URL` environment variable on the web service. The app reads `DATABASE_URL`
   automatically (see `app/database.py`) — no code changes needed.
4. Once your frontend is deployed to Vercel, set `FRONTEND_ORIGIN` on this service to your Vercel URL
   (e.g. `https://oop-dojo.vercel.app`) so CORS only allows your frontend. It defaults to `*` (any origin)
   which is fine to start with.

## Adding more content

Everything you train on lives in `app/content.py` as plain Python dicts — no migrations needed. To add a
topic, copy an existing topic dict inside a level's `topics` list and fill in `theory`, `quiz`, `challenge`
(with `starter_code` and `tests`, where each test is a Python snippet using `assert`), and `interview`
questions. To add a whole new level, copy a level dict at the top level of `LEVELS`.
