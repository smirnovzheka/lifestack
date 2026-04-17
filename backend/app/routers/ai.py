from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.schemas.ai import AiRequest, AiResponse
from app.services.ai_service import build_system_prompt, get_ai_response
from app.services.context_builder import build_full_context, build_project_context, build_routine_context

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=AiResponse)
async def chat(body: AiRequest, db: Session = Depends(get_db)):
    context = build_full_context(db)
    system = build_system_prompt("chat", context)
    history = [m.model_dump() for m in body.history]
    response = await get_ai_response(body.message, system, history)
    return AiResponse(response=response)


@router.post("/project/{project_id}", response_model=AiResponse)
async def project_chat(project_id: int, body: AiRequest, db: Session = Depends(get_db)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    context = build_project_context(project_id, db)
    system = build_system_prompt("project", context)
    history = [m.model_dump() for m in body.history]
    response = await get_ai_response(body.message, system, history)
    return AiResponse(response=response)


@router.post("/routines/analyze", response_model=AiResponse)
async def routines_analyze(body: AiRequest, db: Session = Depends(get_db)):
    context = build_routine_context(db)
    system = build_system_prompt("routines", context)
    history = [m.model_dump() for m in body.history]
    response = await get_ai_response(body.message, system, history)
    return AiResponse(response=response)
