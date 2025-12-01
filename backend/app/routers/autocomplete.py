# backend/app/routers/autocomplete.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.groq_autocomplete import groq_autocomplete  # ✅ IMPORT INSTANCE!

router = APIRouter()

class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

@router.post("/autocomplete")
async def autocomplete_endpoint(request: AutocompleteRequest):
    """✅ AI Autocomplete - Last-write-wins sync ready!"""
    print(f"📥 AI req: lang={request.language}, pos={request.cursorPosition}")
    
    try:
        suggestions = await groq_autocomplete.get_suggestions(
            request.code, 
            request.cursorPosition, 
            request.language
        )
        print(f"📤 {len(suggestions)} suggestions")
        return suggestions
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return []
