from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.groq_autocomplete import groq_autocomplete  # ✅ Correct name
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])

class AutocompleteRequest(BaseModel):
    code: str
    cursor_pos: int

class Suggestion(BaseModel):
    text: str
    type: str

@router.post("", response_model=List[Suggestion])
async def autocomplete_endpoint(request: AutocompleteRequest):
    suggestions = await groq_autocomplete.get_suggestions(  # Async!
        request.code, 
        request.cursor_pos
    )
    return suggestions
