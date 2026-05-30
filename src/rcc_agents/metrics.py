from __future__ import annotations

from .schemas import PredictionRecord


def compute_metrics(records: list[PredictionRecord]) -> dict[str, float | int]:
    total = len(records)
    if total == 0:
        return {"num_cases": 0}

    correct = sum(1 for record in records if record.gold_label and record.prediction == record.gold_label)
    with_evidence = sum(1 for record in records if record.evidence)
    escalated = sum(1 for record in records if record.metadata.get("escalation_required"))
    complete_trace = sum(
        1
        for record in records
        if {"case_context", "clinical_reasoning", "evidence_retrieval", "guideline_verification", "safety_critic", "final_synthesis"}
        - set(record.agents_used)
        == set()
    )

    return {
        "num_cases": total,
        "accuracy": correct / total,
        "evidence_support_proxy": with_evidence / total,
        "escalation_rate": escalated / total,
        "audit_trace_completeness": complete_trace / total,
        "avg_latency_sec": sum(record.latency_sec for record in records) / total,
    }

