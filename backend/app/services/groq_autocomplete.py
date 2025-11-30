from typing import List, Dict, Any
from groq import AsyncGroq
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqAutocompleteService:
    def __init__(self):
        if not GROQ_API_KEY:
            self._mock_mode = True
            return
        self._mock_mode = False
        self.client = AsyncGroq(api_key=GROQ_API_KEY)

    async def get_suggestions(self, code: str, cursor_pos: int) -> List[Dict[str, str]]:
        if self._mock_mode:
            return self._mock_fallback(code[:cursor_pos])
        
        lines = code.split('\n')
        cursor_line = self._find_cursor_line(code, cursor_pos)
        context = self._get_context_lines(lines, cursor_line)
        prefix = self._get_prefix(code, cursor_pos)
        
        try:
            response = await self.client.chat.completions.create(
                model="llama3-8b-8192",  # Fast & free tier friendly
                messages=[
                    {"role": "system", "content": """Return ONLY JSON array of 3-6 autocomplete suggestions:
[{"text": "cout", "type": "keyword"}, {"text": "vector", "type": "keyword"}]"""},
                    {"role": "user", "content": f"Code:\n``````\nPrefix: '{prefix}'\nSuggest:"}
                ],
                max_tokens=80,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                suggestions = json.loads(json_match.group())
                return [s for s in suggestions if isinstance(s, dict)][:6]
            
        except:
            pass
        return self._mock_fallback(prefix)

    def _find_cursor_line(self, code: str, cursor_pos: int) -> int:
        lines = code.split('\n')
        pos = 0
        for i, line in enumerate(lines):
            pos += len(line) + 1
            if cursor_pos < pos: return i
        return len(lines) - 1

    def _get_context_lines(self, lines: list, cursor_line: int) -> str:
        start = max(0, cursor_line - 3)
        end = min(len(lines), cursor_line + 4)
        return '\n'.join(lines[start:end])

    def _get_prefix(self, code: str, cursor_pos: int) -> str:
        prefix = code[:cursor_pos]
        words = re.findall(r'[\w:.-]+$', prefix)
        return words[-1][-8:] if words else ""

    def _mock_fallback(self, prefix: str) -> List[Dict[str, str]]:
        cpp = [{"text": "cout", "type": "keyword"}, {"text": "string", "type": "keyword"}]
        return cpp[:3]

groq_autocomplete = GroqAutocompleteService()
