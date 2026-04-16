from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.routine import Routine, RoutineLog
from app.schemas.routine import (
    RoutineCreate, RoutineOut, RoutineUpdate, RoutineWithLogs,
    RoutineLogCreate, RoutineLogOut, RoutineLogUpdate,
)

router = APIRouter(prefix="/routines", tags=["routines"])


@router.get("/", response_model=list[RoutineOut])
def list_routines(active_only: bool = True, db: Session = Depends(get_db)):
    q = db.query(Routine)
    if active_only:
        q = q.filter(Routine.active == True)  # noqa: E712
    return q.order_by(Routine.created_at).all()


@router.post("/", response_model=RoutineOut, status_code=201)
def create_routine(body: RoutineCreate, db: Session = Depends(get_db)):
    routine = Routine(**body.model_dump())
    db.add(routine)
    db.commit()
    db.refresh(routine)
    return routine


@router.get("/{routine_id}", response_model=RoutineWithLogs)
def get_routine(routine_id: int, db: Session = Depends(get_db)):
    routine = db.get(Routine, routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routine


@router.patch("/{routine_id}", response_model=RoutineOut)
def update_routine(routine_id: int, body: RoutineUpdate, db: Session = Depends(get_db)):
    routine = db.get(Routine, routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(routine, field, value)
    db.commit()
    db.refresh(routine)
    return routine


@router.delete("/{routine_id}", status_code=204)
def delete_routine(routine_id: int, db: Session = Depends(get_db)):
    routine = db.get(Routine, routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    db.delete(routine)
    db.commit()


# --- Logs ---

@router.get("/{routine_id}/logs", response_model=list[RoutineLogOut])
def list_logs(
    routine_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    if not db.get(Routine, routine_id):
        raise HTTPException(status_code=404, detail="Routine not found")
    q = db.query(RoutineLog).filter(RoutineLog.routine_id == routine_id)
    if from_date:
        q = q.filter(RoutineLog.date >= from_date)
    if to_date:
        q = q.filter(RoutineLog.date <= to_date)
    return q.order_by(RoutineLog.date.desc()).all()


@router.post("/{routine_id}/logs", response_model=RoutineLogOut, status_code=201)
def create_log(routine_id: int, body: RoutineLogCreate, db: Session = Depends(get_db)):
    if not db.get(Routine, routine_id):
        raise HTTPException(status_code=404, detail="Routine not found")
    log = RoutineLog(routine_id=routine_id, **body.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.patch("/{routine_id}/logs/{log_id}", response_model=RoutineLogOut)
def update_log(routine_id: int, log_id: int, body: RoutineLogUpdate, db: Session = Depends(get_db)):
    log = db.get(RoutineLog, log_id)
    if not log or log.routine_id != routine_id:
        raise HTTPException(status_code=404, detail="Log not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{routine_id}/logs/{log_id}", status_code=204)
def delete_log(routine_id: int, log_id: int, db: Session = Depends(get_db)):
    log = db.get(RoutineLog, log_id)
    if not log or log.routine_id != routine_id:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
