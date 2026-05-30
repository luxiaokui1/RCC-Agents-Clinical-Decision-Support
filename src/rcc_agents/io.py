from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .schemas import PredictionRecord


def write_jsonl(path: str | Path, records: Iterable[PredictionRecord]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_jsonable(), ensure_ascii=False) + "\n")


def write_json(path: str | Path, payload: object) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

