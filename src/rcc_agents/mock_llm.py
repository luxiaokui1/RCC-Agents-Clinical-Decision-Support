from __future__ import annotations

import re

from .schemas import CaseRecord


class MockClinicalLLM:
    """Deterministic stand-in so the pipeline can run before paid API experiments."""

    def answer_option(self, case: CaseRecord) -> str:
        text = f"{case.question} {' '.join(case.options.values())}".lower()
        if "st-segment" in text or "crushing chest pain" in text:
            return self._find_option(case, "reperfusion")
        if "vitamin deficiency" in text or "scurvy" in text:
            return self._find_option(case, "vitamin c")
        if "wheezing" in text or "bronchodilation" in text:
            return self._find_option(case, "albuterol")
        return next(iter(case.options.keys()), "")

    def summarize_case(self, case: CaseRecord) -> str:
        return f"Structured case summary: {case.question}"

    def retrieve_evidence(self, case: CaseRecord, predicted_label: str) -> str:
        answer = case.options.get(predicted_label, "")
        return f"The selected option is '{answer}', which is directly relevant to the urgent clinical scenario."

    def verify_guideline_alignment(self, case: CaseRecord, predicted_label: str) -> str:
        answer = case.options.get(predicted_label, "")
        return f"No obvious conflict detected for option '{answer}' in this benchmark-style case."

    def safety_review(self, case: CaseRecord, predicted_label: str) -> tuple[str, list[str], bool]:
        risky_terms = ["treatment", "urgent", "chest pain", "st-segment", "reperfusion"]
        text = case.question.lower()
        flags = ["clinician_review_required"] if any(term in text for term in risky_terms) else []
        escalation = bool(flags)
        return "Flagged for clinician review due to potentially high-stakes clinical context.", flags, escalation

    def _find_option(self, case: CaseRecord, needle: str) -> str:
        for label, option in case.options.items():
            if re.search(re.escape(needle), option.lower()):
                return label
        return next(iter(case.options.keys()), "")

