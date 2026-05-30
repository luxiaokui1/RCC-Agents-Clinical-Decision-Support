from __future__ import annotations

import time

from .mock_llm import MockClinicalLLM
from .schemas import CaseRecord, EvidenceSpan, PredictionRecord, RoleMessage


class RCCPipeline:
    def __init__(self, llm: MockClinicalLLM | None = None, method: str = "rcc_mock_full"):
        self.llm = llm or MockClinicalLLM()
        self.method = method

    def run_case(self, case: CaseRecord) -> PredictionRecord:
        if self.method == "single_agent":
            return self._run_single_agent(case)
        if self.method == "rag_only":
            return self._run_rag_only(case)
        if self.method == "homogeneous_multi_agent":
            return self._run_homogeneous_multi_agent(case)
        return self._run_rcc_variant(case)

    def _run_single_agent(self, case: CaseRecord) -> PredictionRecord:
        start = time.perf_counter()
        prediction = self.llm.answer_option(case)
        trace = [
            RoleMessage(
                sender_role="clinical_reasoning",
                receiver_role="final_synthesis",
                case_id=case.case_id,
                message_type="direct_answer",
                content=f"Direct candidate answer: ({prediction}) {case.options.get(prediction, '')}",
                allowed_action="synthesize_without_external_verification",
                evidence_required=False,
                uncertainty="medium",
            )
        ]
        return PredictionRecord(
            case_id=case.case_id,
            method=self.method,
            question=case.question,
            prediction=prediction,
            gold_label=case.gold_label,
            gold_answer=case.gold_answer,
            evidence=[],
            agents_used=["clinical_reasoning", "final_synthesis"],
            audit_trace=trace,
            latency_sec=time.perf_counter() - start,
            metadata={
                "answer_text": case.options.get(prediction, ""),
                "escalation_required": False,
                "risk_flags": [],
            },
        )

    def _run_rag_only(self, case: CaseRecord) -> PredictionRecord:
        start = time.perf_counter()
        prediction = self.llm.answer_option(case)
        reasoning = f"Candidate answer: ({prediction}) {case.options.get(prediction, '')}"
        evidence_text = self.llm.retrieve_evidence(case, prediction)
        evidence = [
            EvidenceSpan(
                source_id=f"{case.case_id}_benchmark_context",
                span=evidence_text,
                claim_supported=reasoning,
            )
        ]
        trace = [
            RoleMessage(
                sender_role="evidence_retrieval",
                receiver_role="final_synthesis",
                case_id=case.case_id,
                message_type="retrieved_context",
                content=evidence_text,
                allowed_action="use_as_support_only",
                evidence_required=True,
                evidence=evidence,
                uncertainty="low",
            )
        ]
        return PredictionRecord(
            case_id=case.case_id,
            method=self.method,
            question=case.question,
            prediction=prediction,
            gold_label=case.gold_label,
            gold_answer=case.gold_answer,
            evidence=evidence,
            agents_used=["evidence_retrieval", "final_synthesis"],
            audit_trace=trace,
            latency_sec=time.perf_counter() - start,
            metadata={
                "answer_text": case.options.get(prediction, ""),
                "escalation_required": False,
                "risk_flags": [],
            },
        )

    def _run_homogeneous_multi_agent(self, case: CaseRecord) -> PredictionRecord:
        start = time.perf_counter()
        prediction = self.llm.answer_option(case)
        reasoning = f"Candidate answer: ({prediction}) {case.options.get(prediction, '')}"
        summary = self.llm.summarize_case(case)
        trace = [
            RoleMessage(
                sender_role="case_context",
                receiver_role="clinical_reasoning",
                case_id=case.case_id,
                message_type="case_summary",
                content=summary,
                allowed_action="use_as_case_context",
                evidence_required=False,
                uncertainty="low",
            ),
            RoleMessage(
                sender_role="clinical_reasoning",
                receiver_role="guideline_verification",
                case_id=case.case_id,
                message_type="candidate_answer",
                content=reasoning,
                allowed_action="discuss_freely",
                evidence_required=False,
                uncertainty="medium",
            ),
            RoleMessage(
                sender_role="guideline_verification",
                receiver_role="final_synthesis",
                case_id=case.case_id,
                message_type="peer_check",
                content=self.llm.verify_guideline_alignment(case, prediction),
                allowed_action="use_for_final_answer",
                evidence_required=False,
                uncertainty="medium",
            ),
        ]
        return PredictionRecord(
            case_id=case.case_id,
            method=self.method,
            question=case.question,
            prediction=prediction,
            gold_label=case.gold_label,
            gold_answer=case.gold_answer,
            evidence=[],
            agents_used=["case_context", "clinical_reasoning", "guideline_verification", "final_synthesis"],
            audit_trace=trace,
            latency_sec=time.perf_counter() - start,
            metadata={
                "answer_text": case.options.get(prediction, ""),
                "escalation_required": False,
                "risk_flags": [],
            },
        )

    def _run_rcc_variant(self, case: CaseRecord) -> PredictionRecord:
        start = time.perf_counter()
        trace: list[RoleMessage] = []
        agents_used = [
            "case_context",
            "evidence_retrieval",
            "clinical_reasoning",
            "guideline_verification",
            "safety_critic",
            "final_synthesis",
        ]
        use_retrieval = self.method != "rcc_no_retrieval"
        use_guideline = self.method != "rcc_no_guideline_verification"
        use_safety = self.method != "rcc_no_safety_critic"
        adaptive_routing = self.method != "rcc_no_adaptive_routing"
        if not use_retrieval:
            agents_used.remove("evidence_retrieval")
        if not use_guideline:
            agents_used.remove("guideline_verification")
        if not use_safety:
            agents_used.remove("safety_critic")

        summary = self.llm.summarize_case(case)
        trace.append(
            RoleMessage(
                sender_role="case_context",
                receiver_role="clinical_reasoning",
                case_id=case.case_id,
                message_type="case_summary",
                content=summary,
                allowed_action="use_as_case_context",
                evidence_required=False,
                uncertainty="low",
            )
        )

        prediction = self.llm.answer_option(case)
        reasoning = f"Candidate answer: ({prediction}) {case.options.get(prediction, '')}"
        trace.append(
            RoleMessage(
                sender_role="clinical_reasoning",
                receiver_role="guideline_verification",
                case_id=case.case_id,
                message_type="candidate_answer",
                content=reasoning,
                allowed_action="verify_before_synthesis",
                evidence_required=True,
                uncertainty="medium",
            )
        )

        evidence: list[EvidenceSpan] = []
        if use_retrieval:
            evidence_text = self.llm.retrieve_evidence(case, prediction)
            evidence = [
                EvidenceSpan(
                    source_id=f"{case.case_id}_benchmark_context",
                    span=evidence_text,
                    claim_supported=reasoning,
                )
            ]
            trace.append(
                RoleMessage(
                    sender_role="evidence_retrieval",
                    receiver_role="clinical_reasoning",
                    case_id=case.case_id,
                    message_type="evidence_packet",
                    content=evidence_text,
                    allowed_action="use_as_support_only",
                    evidence_required=True,
                    evidence=evidence,
                    uncertainty="low",
                )
            )

        if use_guideline:
            guideline_check = self.llm.verify_guideline_alignment(case, prediction)
            trace.append(
                RoleMessage(
                    sender_role="guideline_verification",
                    receiver_role="safety_critic" if use_safety else "final_synthesis",
                    case_id=case.case_id,
                    message_type="verification_result",
                    content=guideline_check,
                    allowed_action="use_for_risk_assessment",
                    evidence_required=use_retrieval,
                    evidence=evidence,
                    uncertainty="medium",
                )
            )

        risk_flags: list[str] = []
        escalation = False
        if use_safety:
            safety_note, risk_flags, escalation = self.llm.safety_review(case, prediction)
            if not adaptive_routing:
                risk_flags = sorted(set(risk_flags + ["always_route_all_modules"]))
            trace.append(
                RoleMessage(
                    sender_role="safety_critic",
                    receiver_role="final_synthesis",
                    case_id=case.case_id,
                    message_type="safety_review",
                    content=safety_note,
                    allowed_action="include_escalation_flag",
                    evidence_required=False,
                    uncertainty="medium",
                    risk_flags=risk_flags,
                    escalation_required=escalation,
                )
            )

        latency = time.perf_counter() - start
        return PredictionRecord(
            case_id=case.case_id,
            method=self.method,
            question=case.question,
            prediction=prediction,
            gold_label=case.gold_label,
            gold_answer=case.gold_answer,
            evidence=evidence,
            agents_used=agents_used,
            audit_trace=trace,
            latency_sec=latency,
            metadata={
                "answer_text": case.options.get(prediction, ""),
                "escalation_required": escalation,
                "risk_flags": risk_flags,
            },
        )
