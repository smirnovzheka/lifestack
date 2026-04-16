from datetime import date, datetime

from pydantic import BaseModel


class RoutineBase(BaseModel):
    name: str
    type: str = "daily"
    unit: str | None = None
    icon: str | None = None


class RoutineCreate(RoutineBase):
    pass


class RoutineUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    unit: str | None = None
    icon: str | None = None
    active: bool | None = None


class RoutineOut(RoutineBase):
    id: int
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RoutineLogBase(BaseModel):
    date: date
    done: bool = False
    value: float | None = None
    note: str | None = None


class RoutineLogCreate(RoutineLogBase):
    pass


class RoutineLogUpdate(BaseModel):
    done: bool | None = None
    value: float | None = None
    note: str | None = None


class RoutineLogOut(RoutineLogBase):
    id: int
    routine_id: int

    model_config = {"from_attributes": True}


class RoutineWithLogs(RoutineOut):
    logs: list[RoutineLogOut] = []
