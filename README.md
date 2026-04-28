# FindBud — AI-Driven Social Matching for Finding the Right Teammate

![Hackathon Prize](https://img.shields.io/badge/Hackathon-3rd%20Prize-brightgreen?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript%20%2B%20Vite-61dafb?style=for-the-badge&logo=react&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![ORM](https://img.shields.io/badge/ORM-SQLAlchemy-d71f00?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-LLM%20API%20(OpenAI--compatible)-8a2be2?style=for-the-badge)

> An agile, full-stack, AI-driven social matching platform that dynamically generates personalized questionnaires and recommends the most compatible teammates based on structured profiling and matching algorithms.

---

## Project Overview

**FindBud** is a campus-oriented teammate matching platform built during our university hackathon, where it won **3rd Prize**.

It addresses a real pain point in student collaboration: finding teammates is easy, but finding the **right** teammates with complementary skills, aligned goals, and compatible working styles is hard.

The current product focuses on **competition teammate matching**, with a strong implementation around **mathematical modeling contests**, while the architecture is designed to be extensible to other scenarios such as study partners.

## My Role & Contributions

As the **full-stack development lead** of the team, I was responsible for turning the hackathon idea into an end-to-end working product across frontend, backend, data flow, and AI integration.

- **Architecture Ownership**
  Designed the overall full-stack architecture connecting the React frontend, FastAPI backend, PostgreSQL database, AI service layer, and matching pipeline.
- **Backend System Design**
  Built the core backend structure with modular routers, schemas, services, ORM models, and migration support, enabling the product to evolve quickly during the hackathon under agile iteration.
- **Frontend-Backend Integration**
  Led the API contract design and integration flow across onboarding, pre-questions, AI-generated questions, answer submission, and final match result rendering.
- **LLM API Integration**
  Implemented the core logic for calling an OpenAI-compatible LLM API to generate dynamic questionnaire content and parse structured JSON responses safely.
- **Prompt Engineering**
  Personally designed the prompt strategy that injects competition context and evaluation dimensions into the model, so the AI asks **targeted, scenario-based, non-generic questions** instead of relying on a static questionnaire bank.
- **Engineering Closure**
  Closed the loop from prompt design to backend orchestration to profile scoring to final recommendation output, demonstrating full ownership of the product from concept to deployable prototype.

---

## Key Features

- **AI-generated personalized questionnaires**
  Instead of using a fixed question bank, the system sends the target scenario and evaluation dimensions to an LLM, which generates contextual and differentiated questions for each session.
- **Adaptive question generation pipeline**
  The backend supports incremental AI question generation, question prewarming, caching, and graceful fallback to MVP questions when the AI service is unavailable.
- **Structured profiling from user choices**
  User answers are transformed into structured profile vectors representing skill tendencies, collaboration style, and ambition-related attributes.
- **Compatibility-aware teammate matching**
  The matching engine combines complementarity and similarity signals, then ranks candidates with a weighted utility function to produce **Top 3** recommendations.
- **Scenario extensibility**
  Although the MVP is optimized for mathematical modeling contests, the codebase already shows extensibility toward additional domains such as IELTS study-partner matching.
- **End-to-end product flow**
  The application covers onboarding, preference collection, AI-driven assessment, and result visualization in a complete full-stack loop.

---

## How the AI Layer Works

- **Context injection**
  The backend injects `competition_type` and `evaluation dimensions` into the system prompt so the LLM understands what kind of teammate assessment it should perform.
- **Prompt-guided generation**
  The model is explicitly instructed to ask scenario-based questions, avoid exposing raw evaluation dimensions directly, and return machine-readable JSON.
- **Session-aware variation**
  Generation includes variation hints and session-level context to avoid repetitive templates and improve diversity across question sets.
- **Profile construction**
  Submitted answers are mapped into structured user profile fields, which become the inputs to the matching service.
- **Ranking output**
  The matching engine computes recommendation scores and returns the best candidates with explanatory summaries and radar-style dimensions.

---

## Tech Stack

- **Frontend**
  - React 18
  - TypeScript
  - Vite
  - React Router
  - Recharts
  - React Select

- **Backend**
  - Python
  - FastAPI
  - Pydantic v2
  - Uvicorn

- **Database & Data Layer**
  - PostgreSQL
  - SQLAlchemy 2
  - Alembic

- **AI / LLM Integration**
  - OpenAI-compatible API client
  - Prompt Engineering for dynamic questionnaire generation
  - JSON-structured response parsing

- **Engineering Workflow**
  - Full-stack API contract integration
  - Agile iteration with fallback-safe product flow

---

## Architecture Snapshot

```text
Frontend (React + Vite)
    -> onboarding / pre-question / ai-question / result
    -> calls REST APIs

Backend (FastAPI)
    -> user_router: user creation + session initialization
    -> question_router: pre-answers, AI question generation, answer submission
    -> ai_service: LLM prompt building + generation
    -> match_service: profile scoring + top match ranking

Database (PostgreSQL)
    -> users
    -> user_profiles / ielts_user_profiles
    -> match_sessions
    -> question_answers / match_results
```

## Quick Start

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 15+ (or any locally available PostgreSQL instance)
- **An OpenAI-compatible API key** for the AI generation module

### 1) Clone the repository

```bash
git clone https://github.com/xiayanghua/FindBud_APP.git
cd FindBud_APP
```

### 2) Start the backend

#### Ubuntu / macOS / Linux

```bash
python -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

Create `backend/.env` manually with the following fields:

```dotenv
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/findbud_db
AI_API_KEY=your_api_key_here
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL_NAME=gpt-4o
DEBUG=True
```

Run database migrations and optional demo seeding:

```bash
createdb findbud_db
cd backend
alembic upgrade head
python scripts/reset_and_seed_demo.py
uvicorn app.main:app --reload --port 8000
```

API docs:

```text
http://localhost:8000/docs
```

#### Windows (PowerShell)

```powershell
python -m venv backend\venv
backend\venv\Scripts\activate
pip install -r backend\requirements.txt

# Create backend/.env manually before running the next steps

createdb findbud_db
alembic -c backend\alembic.ini upgrade head
python backend\scripts\reset_and_seed_demo.py
uvicorn app.main:app --reload --port 8000
```

If the Alembic command on Windows cannot resolve the environment correctly from the project root, run it inside the `backend` directory instead.

### 3) Start the frontend

Create `frontend/.env`:

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

Then run:

```bash
npm install --prefix frontend
npm run dev --prefix frontend
```

Frontend URL:

```text
http://localhost:5173
```

### 4) Health check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "message": "FindBud 后端服务运行正常"
}
```

---

## UI / Demo

> Replace the placeholder below with your own screenshots or demo GIFs.

![Demo Screenshot](link)

---

## Repository Structure

```text
FindBud_APP/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── OnboardingPage.tsx
│   │   │   ├── PreQuestionPage.tsx
│   │   │   ├── AIQuestionPage.tsx
│   │   │   └── MatchResultPage.tsx
│   │   ├── api/
│   │   └── App.tsx
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   ├── alembic/
│   ├── scripts/
│   └── requirements.txt
└── README.md
```

## Why This Project Matters

- **Agile product thinking**
  The system was built as a hackathon prototype but already reflects modular engineering decisions that support iteration and expansion.
- **Full-stack execution**
  The product is not just a UI concept or an isolated model demo; it is a complete, interactive application with real frontend-backend-AI orchestration.
- **AI as product logic, not decoration**
  AI is used as a core decision-support layer for generating differentiated questionnaire content and driving downstream profile construction.

## License

MIT License — see [LICENSE](./LICENSE)
