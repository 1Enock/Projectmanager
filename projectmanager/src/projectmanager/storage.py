import json
from pathlib import Path
from typing import Any


class DataStorage:
    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self.data_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.data_path.exists():
            return {}
        try:
            with self.data_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return {}

    def save(self, data: dict[str, Any]) -> None:
        with self.data_path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
