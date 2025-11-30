# backend/app/routers/autocomplete.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.groq_autocomplete import groq_autocomplete  # ✅ CORRECT IMPORT!

router = APIRouter()

class AutocompleteRequest(BaseModel):
    code: str
    cursor_pos: int

@router.post("/autocomplete")
async def autocomplete_endpoint(request: AutocompleteRequest):
    suggestions = await groq_autocomplete.get_suggestions(request.code, request.cursor_pos)
    return suggestions
