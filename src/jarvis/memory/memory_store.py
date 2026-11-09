from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class MemoryStore:
    def __init__(self, storage_path: str | Path):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text("{}", encoding="utf-8")

    def _read(self) -> Dict[str, Any]:
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
        return {}

    def _write(self, data: Dict[str, Any]) -> None:
        self.storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def remember(self, user_id: str, memory: str) -> None:
        data = self._read()
        memories = data.setdefault(user_id, [])
        if not isinstance(memories, list):
            memories = []
        memories.append(memory)
        data[user_id] = memories
        self._write(data)

    def get_memory(self, user_id: str) -> List[str]:
        return self._read().get(user_id, [])

    def list_all(self) -> Dict[str, List[str]]:
        return self._read()
