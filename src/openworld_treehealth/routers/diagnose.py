from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services import openai_client

router = APIRouter(prefix="/diagnose", tags=["diagnose"])


class DiagnoseRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=2000)
    location: Optional[str] = Field(None, max_length=200)


class DiagnoseResponse(BaseModel):
    diagnosis: str
    safety_note: str


SYSTEM_PROMPT = (
    "You are an arborist. Provide concise, practical tree health guidance. "
    "Avoid medical claims. Suggest next steps and safety cautions."
)


@router.post("/", response_model=DiagnoseResponse)
async def diagnose(payload: DiagnoseRequest) -> DiagnoseResponse:
    client = openai_client.get_openai_client()
    if client is None:
        raise HTTPException(status_code=503, detail="OpenAI not configured")

    user_prompt = f"Location: {payload.location or 'unknown'}\nObservations: {payload.description}"

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_prompt}],
            },
        ],
        max_output_tokens=300,
    )

    text = response.output_text
    return DiagnoseResponse(
        diagnosis=text.strip(),
        safety_note="Consult a certified arborist for on-site assessment if uncertainty remains.",
    )


