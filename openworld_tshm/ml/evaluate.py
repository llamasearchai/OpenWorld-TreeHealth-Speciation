from __future__ import annotations
import json
from typing import Any


def load_metrics(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


