# Paper Plan

## Title

Role-Conditioned Communication for Auditable Heterogeneous LLM Agents in Clinician-in-the-Loop Decision Support: A Modular Framework and Ablation Study

## One-Sentence Thesis

Clinical LLM agents should not only be assigned roles; their communication should be explicitly conditioned on role, evidence requirements, risk level, and escalation rules so that heterogeneous agent collaboration becomes auditable, modular, and clinically safer to review.

## Positioning

This paper is not claiming to introduce the first clinical multi-agent LLM system. Prior work already studies medical agents, role-playing agents, adaptive medical collaboration, and mixed-vendor LLM councils.

The paper focuses on a narrower gap: how heterogeneous agents communicate, what evidence they are required to attach, when extra modules are activated, and how each module affects reliability under ablation.

## Proposed Contributions

1. A role-conditioned communication protocol for heterogeneous LLM agents in clinician-in-the-loop decision support.

2. A modular agent framework with explicit add/remove components: retrieval, clinical reasoning, guideline verification, safety critique, uncertainty estimation, and final synthesis.

3. An ablation-driven evaluation showing how each module affects accuracy, evidence support, hallucination rate, unsafe recommendation rate, abstention behavior, cost, and latency.

4. An audit trace format that records agent roles, evidence links, disagreements, escalation triggers, and final synthesis rationale for human review.

## System Modules

### 1. Case Context Agent

Summarizes the input case into structured fields:
- patient context
- symptoms or question
- relevant history
- missing information
- task type

### 2. Evidence Retrieval Agent

Retrieves supporting material from trusted sources or datasets. In early experiments, this can use benchmark-provided context, PubMed abstracts, guideline excerpts, or curated documents.

### 3. Clinical Reasoning Agent

Produces candidate reasoning paths and answer options, but must cite evidence spans or mark unsupported claims.

### 4. Guideline Verification Agent

Checks whether the candidate answer conflicts with provided guideline evidence or retrieved references.

### 5. Safety Critic Agent

Flags unsafe, overconfident, unsupported, or treatment-like recommendations. It can recommend abstention or clinician escalation.

### 6. Final Synthesis Agent

Combines the prior outputs into a concise clinician-facing support response with:
- final answer or recommendation class
- supporting evidence
- uncertainty
- escalation flag
- audit trace summary

## Role-Conditioned Communication Protocol

Every inter-agent message should include:

```json
{
  "sender_role": "evidence_retrieval",
  "receiver_role": "clinical_reasoning",
  "case_id": "example_001",
  "message_type": "evidence_packet",
  "allowed_action": "use_as_support_only",
  "evidence_required": true,
  "evidence": [
    {
      "source_id": "doc_01",
      "span": "...",
      "claim_supported": "..."
    }
  ],
  "uncertainty": "medium",
  "risk_flags": [],
  "escalation_required": false
}
```

The key idea is that an agent's output is not free-form conversation. Its role constrains what it may say, what evidence it must attach, and what downstream agents are allowed to do with it.

## Add/Remove Module Ablation

The add/remove module design is central to the paper.

| Setting | Description | Purpose |
|---|---|---|
| Single Agent | One LLM answers directly | Basic baseline |
| RAG Only | Retrieval plus final answer | Tests evidence grounding without agent collaboration |
| Homogeneous Multi-Agent | Same model, multiple roles | Tests role prompting without model diversity |
| Heterogeneous Multi-Agent | Different model families, multiple roles | Tests model diversity |
| Full RCC System | Heterogeneous agents plus role-conditioned communication | Main method |
| Full - Retrieval | Remove retrieval module | Tests evidence grounding contribution |
| Full - Guideline Verification | Remove guideline checker | Tests guideline consistency contribution |
| Full - Safety Critic | Remove safety module | Tests unsafe output reduction |
| Full - Adaptive Routing | Always run all modules | Tests cost/latency benefit of adaptive activation |

## Candidate Datasets

Start with accessible public benchmarks:

- PubMedQA: biomedical question answering with context.
- MedQA: USMLE-style medical QA.
- MedMCQA: large-scale multiple-choice medical QA.
- Medical guideline or clinical note summarization datasets if available and safe.

For the first prototype, PubMedQA is a good starting point because evidence context is easier to attach and audit.

## Metrics

Primary:
- answer accuracy
- evidence support rate
- hallucination rate
- unsafe recommendation rate

Secondary:
- abstention precision
- escalation quality
- disagreement rate
- token cost
- latency
- audit trace completeness

## Expected Paper Structure

1. Introduction
2. Related Work
3. Problem Formulation
4. Role-Conditioned Communication Framework
5. Modular Agent Architecture
6. Experimental Setup
7. Results and Ablation Study
8. Audit Trace Case Studies
9. Limitations and Safety Considerations
10. Conclusion

## Safety Framing

The system is a decision-support research prototype. It should not be described as autonomous diagnosis or autonomous treatment recommendation. All outputs are framed as evidence-grounded assistance for clinician review.
