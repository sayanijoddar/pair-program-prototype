# backend/app/services/groq_autocomplete.py
from typing import List, Dict
import re

# ✅ SINGLE GLOBAL INSTANCE
groq_autocomplete = None

class GroqAutocompleteService:
    def __init__(self):
        print("✅ Mock AI Autocomplete ready (Python-focused!)")

    def _get_prefix(self, code: str, cursor_pos: int) -> str:
        """Extract word prefix before cursor"""
        prefix = code[:cursor_pos]
        words = re.findall(r'[\w_]+$', prefix)
        return words[-1].lower() if words else ""

    async def get_suggestions(self, code: str, cursor_pos: int, language: str = "python") -> List[Dict]:
        prefix = self._get_prefix(code, cursor_pos)
        print(f"🤖 AI: lang='{language}', prefix='{prefix}'")

        # Python-focused suggestions
        python_suggestions = [
            {"text": "print", "type": "keyword", "description": "Print to console"},
            {"text": "len", "type": "function", "description": "Get length"},
            {"text": "list", "type": "keyword", "description": "List type"},
            {"text": "dict", "type": "keyword", "description": "Dictionary type"},
            {"text": "def", "type": "keyword", "description": "Define function"},
            {"text": "if", "type": "keyword", "description": "Conditional"},
            {"text": "for", "type": "keyword", "description": "For loop"},
            {"text": "import", "type": "keyword", "description": "Import module"},
            {"text": "class", "type": "keyword", "description": "Define class"},
            {"text": "return", "type": "keyword", "description": "Return value"},
        ]

        # Filter by prefix (case-insensitive)
        filtered = [s for s in python_suggestions if prefix in s["text"].lower() or not prefix]
        return filtered[:8]

# ✅ EXPORT SINGLE INSTANCE
groq_autocomplete = GroqAutocompleteService()
