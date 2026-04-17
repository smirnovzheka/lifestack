import json

import anthropic

from app.config import settings

MODEL = "claude-sonnet-4-5-20251001"
MAX_TOKENS = 1024
TIMEOUT = 30.0

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def get_ai_response(
    user_message: str,
    system_prompt: str,
    conversation_history: list[dict],
) -> str:
    messages = [
        *conversation_history,
        {"role": "user", "content": user_message},
    ]

    response = _client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=messages,
        timeout=TIMEOUT,
    )

    return response.content[0].text


def build_system_prompt(module: str, context: dict) -> str:
    context_json = json.dumps(context, ensure_ascii=False, default=str)

    prompts = {
        "project": (
            "You are a focused project assistant. You have full context of this specific project: "
            "its goals, all tasks (completed and pending), notes, and timeline. "
            "Give concrete, actionable advice. Be direct. No generic productivity tips. "
            f"Current project context: {context_json}"
        ),
        "routines": (
            "You are analyzing personal health and habit data. You have recent routine logs. "
            "Identify real patterns, streaks, and gaps. Be honest about what the data shows. "
            f"Do not be motivational — be analytical. Context: {context_json}"
        ),
        "chat": (
            "You are a personal life assistant with full context of the user's projects, "
            "tasks, and daily routines. Give clear, direct answers. "
            f"User context: {context_json}"
        ),
    }

    return prompts.get(module, prompts["chat"])
