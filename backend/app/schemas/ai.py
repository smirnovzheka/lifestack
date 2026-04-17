from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class AiRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class AiResponse(BaseModel):
    response: str
