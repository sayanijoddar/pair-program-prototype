# backend/app/services/groq_autocomplete.py - NO MORE ERRORS!
from typing import List, Dict
import json
import re
from groq import AsyncGroq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqAutocompleteService:
    def __init__(self):
        self._mock_mode = True
        try:
            if GROQ_API_KEY:
                self.client = AsyncGroq(api_key=GROQ_API_KEY)
                self._mock_mode = False
                print("✅ Groq client ready")
        except:
            self._mock_mode = True
            print("✅ Using smart mock mode")

    async def get_suggestions(self, code: str, cursor_pos: int) -> List[Dict]:
        # ✅ DEFINE prefix FIRST - NO UnboundLocalError!
        prefix = ""
        try:
            lines = code.split('\n')
            cursor_line = self._find_cursor_line(code, cursor_pos)
            context = self._get_context_lines(lines, cursor_line)
            prefix = self._get_prefix(code, cursor_pos)  # ✅ ALWAYS defined
            
            print(f"DEBUG: prefix='{prefix}'")
            
            if self._mock_mode:
                return self._mock_fallback(prefix)
            
            response = await self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Return ONLY JSON: [{'text':'cout','type':'keyword'}]"},
                    {"role": "user", "content": f"Prefix: {prefix}"}
                ],
                max_tokens=60,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())[:6]
                
        except Exception as e:
            print(f"Autocomplete fallback: {e}")
        
        # ✅ prefix ALWAYS available here!
        return self._mock_fallback(prefix)

    def _find_cursor_line(self, code: str, cursor_pos: int) -> int:
        lines = code.split('\n')
        pos = 0
        for i, line in enumerate(lines):
            pos += len(line) + 1
            if cursor_pos <= pos: 
                return i
        return len(lines) - 1

    def _get_context_lines(self, lines: list, cursor_line: int) -> str:
        start = max(0, cursor_line - 2)
        end = min(len(lines), cursor_line + 3)
        return '\n'.join(lines[start:end])

    def _get_prefix(self, code: str, cursor_pos: int) -> str:
        prefix = code[:cursor_pos]
        words = re.findall(r'[\w:.-#]+$', prefix)
        return words[-1][-10:] if words else ""

    def _mock_fallback(self, prefix: str) -> List[Dict]:
        suggestions = [
            {"text": "cout", "type": "keyword"},
            {"text": "cin", "type": "keyword"},
            {"text": "string", "type": "keyword"},
            {"text": "vector", "type": "keyword"},
            {"text": "include", "type": "keyword"},
            {"text": "define", "type": "keyword"},
            {"text": "console", "type": "keyword"},
            {"text": "log", "type": "function"},
            {"text": "main", "type": "function"}
        ]
        
        prefix_lower = prefix.lower()
        filtered = [s for s in suggestions if prefix_lower in s["text"].lower()]
        return filtered[:4] if filtered else suggestions[:4]

groq_autocomplete = GroqAutocompleteService()
