from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.project import Project, Task
from app.models.routine import Routine, RoutineLog


def build_project_context(project_id: int, db: Session) -> dict:
    project = db.get(Project, project_id)
    if not project:
        return {}

    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    notes = db.query(Note).filter(Note.project_id == project_id).order_by(Note.created_at.desc()).limit(10).all()
    done = [t for t in tasks if t.done]

    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "category": project.category,
            "created_at": str(project.created_at.date()),
        },
        "tasks": {
            "total": len(tasks),
            "done": len(done),
            "pending": [{"id": t.id, "title": t.title, "priority": t.priority} for t in tasks if not t.done],
            "completed": [{"id": t.id, "title": t.title} for t in done],
        },
        "notes": [{"content": n.content, "tags": n.tags, "date": str(n.created_at.date())} for n in notes],
    }


def build_routine_context(db: Session, days: int = 30) -> dict:
    since = date.today() - timedelta(days=days)
    routines = db.query(Routine).filter(Routine.active == True).all()  # noqa: E712

    result = []
    for r in routines:
        logs = (
            db.query(RoutineLog)
            .filter(RoutineLog.routine_id == r.id, RoutineLog.date >= since)
            .order_by(RoutineLog.date.desc())
            .all()
        )
        done_count = sum(1 for l in logs if l.done)
        streak = _calc_streak(logs)

        result.append({
            "id": r.id,
            "name": r.name,
            "unit": r.unit,
            "icon": r.icon,
            "logs_count": len(logs),
            "done_count": done_count,
            "completion_rate": round(done_count / days * 100) if days else 0,
            "current_streak": streak,
            "recent_logs": [
                {"date": str(l.date), "done": l.done, "value": l.value, "note": l.note}
                for l in logs[:7]
            ],
        })

    return {"period_days": days, "routines": result}


def build_full_context(db: Session) -> dict:
    projects = db.query(Project).all()
    projects_summary = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "tasks_total": len(p.tasks),
            "tasks_done": sum(1 for t in p.tasks if t.done),
        }
        for p in projects
    ]

    return {
        "projects": projects_summary,
        "routines": build_routine_context(db, days=14),
        "today": str(date.today()),
    }


def _calc_streak(logs: list[RoutineLog]) -> int:
    if not logs:
        return 0
    streak = 0
    check_date = date.today()
    logs_by_date = {l.date: l for l in logs}
    while True:
        log = logs_by_date.get(check_date)
        if log and log.done:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    return streak
