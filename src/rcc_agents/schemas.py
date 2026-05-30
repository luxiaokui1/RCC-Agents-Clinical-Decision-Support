from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class EvidenceSpan:
    source_id: str
    span: str
    claim_supported: str


@dataclass
class RoleMessage:
    sender_role: str
    receiver_role: str
    case_id: str
    message_type: str
    content: str
    allowed_action: str
    evidence_required: bool
    evidence: list[EvidenceSpan] = field(default_factory=list)
    uncertainty: str = "unknown"
    risk_flags: list[str] = field(default_factory=list)
    escalation_required: bool = False


@dataclass
class CaseRecord:
    case_id: str
    question: str
    options: dict[str, str]
    gold_label: str | None = None
    gold_answer: str | None = None
    context: str | None = None


@dataclass
class PredictionRecord:
    case_id: str
    method: str
    question: str
    prediction: str
    gold_label: str | None
    gold_answer: str | None
    evidence: list[EvidenceSpan]
    agents_used: list[str]
    audit_trace: list[RoleMessage]
    latency_sec: float
    cost_estimate: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)

