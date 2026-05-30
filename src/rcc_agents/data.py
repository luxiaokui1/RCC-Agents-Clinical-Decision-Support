from __future__ import annotations

import json
from pathlib import Path

from .schemas import CaseRecord


def load_medqa_jsonl(path: str | Path, limit: int | None = None) -> list[CaseRecord]:
    records: list[CaseRecord] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if limit is not None and index >= limit:
                break
            if not line.strip():
                continue
            raw = json.loads(line)
            records.append(
                CaseRecord(
                    case_id=f"medqa_{index:05d}",
                    question=raw["question"],
                    options=raw.get("options", {}),
                    gold_label=raw.get("answer_idx"),
                    gold_answer=raw.get("answer"),
                    context=raw.get("context"),
                )
            )
    return records

