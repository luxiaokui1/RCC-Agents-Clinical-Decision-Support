from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from .io import write_jsonl
from .schemas import PredictionRecord, RoleMessage


ANSWER_RE = re.compile(r"Answer:\s*\(?([A-Z])\)?", re.IGNORECASE)


def extract_prediction(response: object) -> str:
    text = json.dumps(response, ensure_ascii=False) if not isinstance(response, str) else response
    match = ANSWER_RE.search(text)
    if match:
        return match.group(1).upper()
    option_match = re.search(r"\(([A-Z])\)", text)
    return option_match.group(1).upper() if option_match else ""


def wrap_record(raw: dict, index: int, method: str) -> PredictionRecord:
    case_id = f"mdagents_medqa_{index:05d}"
    prediction = extract_prediction(raw.get("response", ""))
    trace = [
        RoleMessage(
            sender_role="mdagents_baseline",
            receiver_role="rcc_evaluator",
            case_id=case_id,
            message_type="baseline_output",
            content=json.dumps(raw.get("response", ""), ensure_ascii=False),
            allowed_action="evaluate_only",
            evidence_required=False,
            uncertainty="unknown",
        )
    ]
    return PredictionRecord(
        case_id=case_id,
        method=method,
        question=raw.get("question", ""),
        prediction=prediction,
        gold_label=raw.get("label"),
        gold_answer=raw.get("answer"),
        evidence=[],
        agents_used=["mdagents_baseline"],
        audit_trace=trace,
        latency_sec=0.0,
        metadata={
            "source": "MDAgents",
            "difficulty": raw.get("difficulty"),
            "wrapped_at_unix": time.time(),
            "raw_options": raw.get("options", {}),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Wrap MDAgents JSON output into RCC prediction JSONL.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="outputs/predictions/mdagents_wrapped.jsonl")
    parser.add_argument("--method", default="mdagents")
    args = parser.parse_args()

    raw_records = json.loads(Path(args.input).read_text(encoding="utf-8"))
    wrapped = [wrap_record(raw, index, args.method) for index, raw in enumerate(raw_records)]
    write_jsonl(args.output, wrapped)
    print(f"Wrote wrapped output: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()

