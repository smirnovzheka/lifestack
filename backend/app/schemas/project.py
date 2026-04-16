from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    priority: str = "medium"
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
    priority: str | None = None
    due_date: datetime | None = None


class TaskOut(TaskBase):
    id: int
    project_id: int
    done: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    category: str
    color: str = "#6366f1"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    color: str | None = None


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: list[TaskOut] = []

    model_config = {"from_attributes": True}


class ProjectList(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks_total: int = 0
    tasks_done: int = 0

    model_config = {"from_attributes": True}
