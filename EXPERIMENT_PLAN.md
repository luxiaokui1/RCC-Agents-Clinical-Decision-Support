# Experiment Plan

## Goal

Build a small, reproducible prototype that tests whether role-conditioned communication improves the reliability and auditability of heterogeneous LLM agents for clinician-in-the-loop decision support.

## Phase 1: Lightweight Prototype

Use a public medical QA dataset with evidence context. PubMedQA is the recommended first target because it supports evidence-grounded evaluation more naturally than pure multiple-choice exams.

### Inputs

- question
- context or abstract
- gold answer
- optional explanation or evidence span if available

### Outputs

- final answer
- supporting evidence
- uncertainty label
- safety or escalation flag
- structured audit trace

## Phase 2: Baselines

Implement these baselines first:

1. Single Agent
   - One model answers directly from the question and context.

2. RAG Only
   - A retrieval/evidence step feeds one answer generator.

3. Homogeneous Multi-Agent
   - Multiple role prompts use the same model.

4. Heterogeneous Multi-Agent
   - Different roles can use different models or different local/API endpoints.

5. Full Role-Conditioned Communication
   - Agents communicate through structured role-conditioned messages.

## Phase 3: Module Ablations

Run the full system and then remove one module at a time:

- Full - Evidence Retrieval
- Full - Guideline Verification
- Full - Safety Critic
- Full - Uncertainty Estimator
- Full - Adaptive Routing

Each ablation should produce the same output schema so metrics are comparable.

## Phase 4: Metrics

### Task Metrics

- accuracy
- macro F1 if labels are imbalanced
- calibration proxy based on confidence/uncertainty

### Evidence Metrics

- evidence support rate
- unsupported claim count
- citation/context mismatch rate

### Safety Metrics

- unsafe recommendation rate
- overconfident unsupported answer rate
- appropriate abstention rate
- escalation precision

### System Metrics

- latency
- token cost
- number of activated modules
- audit trace completeness

## Phase 5: Case Study Analysis

Select 5-10 cases:

- cases where the full system fixes a single-agent error
- cases where the safety critic prevents overclaiming
- cases where retrieval introduces noise
- cases where heterogeneous agents disagree
- cases where the system correctly abstains

## Minimal Implementation Plan

Recommended repository layout:

```text
ARIS-paper-workspace/
  src/
    rcc_agents/
      schemas.py
      agents.py
      router.py
      protocols.py
      metrics.py
      run_experiment.py
  data/
    raw/
    processed/
  outputs/
    traces/
    predictions/
    tables/
  paper/
    main.tex
```

## Codebase Strategy

This project should not be built as a purely hand-written demo from scratch.

Use existing peer-reviewed/open-source medical multi-agent code as baselines and reference implementations:

1. MedAgents
   - Paper: ACL Findings 2024, "MedAgents: Large Language Models as Collaborators for Zero-shot Medical Reasoning"
   - Code: https://github.com/gersteinlab/MedAgents
   - Use as the role-playing multi-agent collaboration baseline.

2. MDAgents
   - Paper: NeurIPS 2024, "MDAgents: An Adaptive Collaboration of LLMs for Medical Decision-Making"
   - Code: https://github.com/mitmedialab/MDAgents
   - Use as the adaptive collaboration baseline and closest prior work.

Our implementation should add a new RCC layer on top of or beside these baselines:

- standardized message schema
- sender/receiver role constraints
- evidence requirement checks
- module activation and removal switches
- audit trace output
- comparable evaluation scripts

This makes the contribution look like a research extension and systematic evaluation, not only a standalone engineering prototype.

## First Small Run

Start with 50-100 examples before scaling:

```text
Dataset: PubMedQA
Models: start with one locally available or API-backed model
Baseline: single-agent vs full RCC prototype
Output: predictions JSONL + audit traces + preliminary metric table
```

## Risks

- Clinical claims may be too strong. Keep all outputs framed as decision support.
- Public datasets may not fully represent real clinical decision support. Acknowledge this as a limitation.
- Heterogeneous model APIs may be expensive. Start with homogeneous roles, then add heterogeneous models once the pipeline works.
- Evidence support scoring may need heuristic or LLM-judge evaluation. Keep a small manually inspected subset for validation.
