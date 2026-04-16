from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str
    project_id: int | None = None
    tags: list[str] = []


class NoteUpdate(BaseModel):
    content: str | None = None
    tags: list[str] | None = None
    project_id: int | None = None


class NoteOut(BaseModel):
    id: int
    content: str
    project_id: int | None
    tags: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}
