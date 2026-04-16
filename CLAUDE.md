# LifeStack — Personal AI Assistant

## Project overview

Personal life management assistant with AI deeply integrated into every module.
Not a chatbot with a sidebar — AI is a participant in each module with its own context.

Goals:
1. Personal daily tool
2. Public GitHub portfolio piece
3. Potential open source product (anyone can self-host in 5 minutes)

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, SQLite |
| Frontend | React 18, Vite, Tailwind CSS |
| AI | Anthropic Claude API (`claude-sonnet-4-5-20251001`) |
| Scheduling | APScheduler (daily briefing cron) |
| Deploy | Docker Compose (backend + frontend + nginx) |
| Auth | Single-user, Bearer token via `.env` |

---

## Repository structure

```
lifestack/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py              # settings from .env
│   │   ├── db/
│   │   │   ├── base.py            # SQLAlchemy Base + engine
│   │   │   └── session.py         # get_db dependency
│   │   ├── models/
│   │   │   ├── project.py         # Project, Task
│   │   │   ├── routine.py         # Routine, RoutineLog
│   │   │   ├── weekly.py          # WeeklyGoal
│   │   │   └── note.py            # Note
│   │   ├── routers/
│   │   │   ├── projects.py
│   │   │   ├── routines.py
│   │   │   ├── weekly.py
│   │   │   ├── notes.py
│   │   │   └── ai.py              # all AI endpoints
│   │   └── services/
│   │       ├── ai_service.py      # core Claude API logic
│   │       ├── context_builder.py # builds context per module
│   │       └── scheduler.py       # daily briefing cron
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/                   # axios wrappers per module
│   │   ├── components/
│   │   │   ├── layout/            # AppShell, Sidebar, TopBar
│   │   │   ├── ai/                # AiPanel, AiChat, AiBadge
│   │   │   └── ui/                # shared primitives
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx      # weekly overview
│   │   │   ├── Routines.jsx       # daily checklist
│   │   │   ├── Projects.jsx       # project list
│   │   │   ├── ProjectDetail.jsx  # single project + tasks + AI
│   │   │   └── Chat.jsx           # full context AI chat
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── CLAUDE.md                      # this file
└── README.md
```

---

## Data models

### Project
```python
id, name, description, category, color, created_at, updated_at
# category: "work" | "pet_project" | "health" | "personal" | "finance"
```

### Task
```python
id, project_id, title, done, priority, due_date, created_at
```

### Routine
```python
id, name, type, unit, icon, active, created_at
# type: "daily" | "weekly"
# examples: "Vitamins", "Workout", "Read 20 pages"
```

### RoutineLog
```python
id, routine_id, date, done, note
```

### WeeklyGoal
```python
id, week_start, title, project_id (nullable), done, created_at
```

### Note
```python
id, project_id (nullable), content, tags, created_at
```

---

## AI integration — core principle

**Every module has its own context builder.** When a user asks AI anything, we don't send a generic prompt — we build a rich context object specific to that module and pass it to Claude.

### AI service interface

```python
# services/ai_service.py
async def get_ai_response(
    user_message: str,
    module_context: dict,      # built by context_builder per module
    conversation_history: list # last N messages for continuity
) -> str
```

### Context builder — per module

```python
# services/context_builder.py

def build_project_context(project_id: int, db) -> dict:
    # Returns: project details, all tasks (done/pending),
    # recent notes, completion %, days since created
    
def build_routine_context(db) -> dict:
    # Returns: all active routines, last 30 days of logs,
    # current streaks, missed patterns
    
def build_weekly_context(db) -> dict:
    # Returns: current week goals, progress,
    # last 4 weeks summary for trend analysis

def build_full_context(db) -> dict:
    # Returns: everything above combined
    # Used for: main chat, daily briefing
```

### AI endpoints (routers/ai.py)

```
POST /api/ai/chat              — full context chat
POST /api/ai/project/{id}      — project-specific analysis
POST /api/ai/routines/analyze  — health/habit analysis
POST /api/ai/weekly/review     — weekly progress review
POST /api/ai/briefing          — generate daily briefing
```

### System prompts — per module

Each module gets a tailored system prompt. Examples:

**Project assistant:**
```
You are a focused project assistant. You have full context of this specific project:
its goals, all tasks (completed and pending), notes, and timeline.
Give concrete, actionable advice. Be direct. No generic productivity tips.
Current project context: {context_json}
```

**Routine / health assistant:**
```
You are analyzing personal health and habit data. You have 30 days of routine logs.
Identify real patterns, streaks, and gaps. Be honest about what the data shows.
Do not be motivational — be analytical. Context: {context_json}
```

**Weekly review:**
```
You are conducting a weekly performance review. You have this week's goals,
what was completed, what was skipped, and trends from previous weeks.
Give a clear assessment and 3 specific priorities for next week. Context: {context_json}
```

---

## API design

All endpoints return consistent shape:
```json
{
  "data": {},
  "error": null
}
```

CRUD follows REST conventions. AI endpoints are always POST with body:
```json
{
  "message": "string",
  "history": [{"role": "user"|"assistant", "content": "string"}]
}
```

---

## Frontend — UI principles

- Clean, dark-friendly design (Tailwind dark mode)
- Every page has an AI panel on the right (collapsible)
- AI panel is context-aware — it already knows what page you're on
- Streaks and progress shown visually (progress bars, heatmap for routines)
- No unnecessary modals — inline editing where possible

### Page structure
```
AppShell
├── Sidebar (navigation)
├── Main content area
│   └── [page-specific content]
└── AiPanel (right, collapsible, 320px)
    ├── Context summary (what AI knows)
    ├── Chat messages
    └── Input
```

---

## Docker setup

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    volumes: ["./data:/app/data"]   # SQLite persists here
    env_file: .env

  frontend:
    build: ./frontend
    ports: ["3000:3000"]

  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    # proxies /api → backend, / → frontend
```

---

## .env.example

```env
ANTHROPIC_API_KEY=sk-ant-...
API_TOKEN=your-secret-token-here
DATABASE_URL=sqlite:///./data/lifestack.db
CORS_ORIGINS=http://localhost:3000,http://localhost
```

---

## Development startup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Or everything at once
docker-compose up --build
```

---

## Build order (suggested)

1. Backend models + DB setup
2. CRUD routers (no AI yet) — get data layer working
3. AI service + context builders
4. AI endpoints
5. Frontend scaffold (AppShell + routing)
6. Pages one by one: Dashboard → Routines → Projects → Chat
7. AiPanel component — wire to each page
8. Docker Compose + nginx
9. README.md

---

## Code quality expectations

- Type hints everywhere in Python
- Pydantic schemas for all request/response models (separate from SQLAlchemy models)
- Async throughout FastAPI
- React components functional only, hooks for state
- No `any` in JS — prop types or TypeScript if you prefer
- Every AI call has error handling and timeout (30s)
- Sensitive data never logged
