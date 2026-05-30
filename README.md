# RCC Agents: Auditable Multi-Agent Clinical Decision Support Prototype

This repository contains a research prototype for **Role-Conditioned Communication (RCC)**, a modular multi-agent LLM framework for clinician-in-the-loop decision support.

The project studies whether medical question answering systems become more auditable and safer to review when agent communication is explicitly constrained by role, evidence requirements, risk flags, and escalation rules.

> This is a research prototype. It is not a medical product, not a diagnosis system, and not a replacement for clinicians.

## What This Project Is

The system takes a medical QA-style case and routes it through several specialized agent roles:

- `case_context`: summarizes the case context.
- `evidence_retrieval`: attaches supporting evidence or benchmark context.
- `clinical_reasoning`: proposes an answer.
- `guideline_verification`: checks whether the answer aligns with available evidence.
- `safety_critic`: flags unsafe, unsupported, or overconfident outputs.
- `final_synthesis`: produces the final answer with audit metadata.

Each step emits a structured `RoleMessage`, so the final prediction includes an audit trace instead of only a free-form answer.

## What Problem It Solves

Many medical LLM systems answer directly or use loosely coordinated agents. This project focuses on a narrower research question:

> Can role-conditioned, evidence-aware communication make heterogeneous clinical LLM agents easier to audit and safer to evaluate?

The current prototype lets us compare:

- direct single-agent answering
- RAG-only answering
- homogeneous multi-agent prompting
- full RCC communication
- RCC with key modules removed

This supports ablation studies that ask which parts of the system actually contribute to evidence support, safety escalation, and audit trace completeness.

## Does It Have a UI?

No. The current version is a command-line research prototype.

It does not include a web frontend, dashboard, or chat interface yet. Outputs are written as JSONL/JSON files under:

```text
outputs/predictions/
outputs/tables/
```

A future UI could visualize each agent message, evidence span, safety flag, and final answer.

## Does It Have Storage?

There is no database in the current prototype.

The project uses file-based storage:

- input cases: `baselines/data/medqa/*.jsonl`
- predictions and audit traces: `outputs/predictions/*.jsonl`
- metrics: `outputs/tables/*.json`
- research state: `ARIS_PROGRESS.md`, `MANIFEST.md`, `research-wiki/`

This keeps the experiment reproducible and lightweight while the research design is still evolving.

## Does It Use AI?

The current code uses a deterministic `MockLLM` backend for no-cost smoke tests.

That means the agent roles, communication protocol, schemas, and metrics are implemented, but the current results are not produced by real model calls yet. The real AI integration points are already represented by methods such as:

- answer selection
- case summarization
- evidence retrieval
- guideline/evidence alignment checking
- safety review
- final synthesis

The next research step is to replace the mock backend with an API or local model backend and evaluate on a larger PubMedQA/MedQA/MedMCQA slice.

## Why This Is Useful

The project is useful as a research and engineering scaffold for:

- studying medical multi-agent LLM collaboration
- comparing single-agent, RAG, and multi-agent baselines
- measuring audit trace completeness
- testing the contribution of retrieval, guideline verification, and safety review
- generating structured experiment outputs for paper writing

It is especially focused on **auditable clinical support**, not autonomous medical decision-making.

## Current Status

The project has:

- a research brief
- novelty positioning
- experiment plan
- paper plan
- deterministic RCC prototype
- baseline and ablation runner
- four-case mock evaluation set
- generated smoke-test metrics

Latest progress is summarized in:

```text
ARIS_PROGRESS.md
```

## Quick Start

From this directory:

```bash
python3 -m src.rcc_agents.run_ablation_suite \
  --input baselines/data/medqa/rcc_mock_eval.jsonl
```

The suite runs:

- `single_agent`
- `rag_only`
- `homogeneous_multi_agent`
- `rcc_mock_full`
- `rcc_no_retrieval`
- `rcc_no_guideline_verification`
- `rcc_no_safety_critic`
- `rcc_no_adaptive_routing`

Outputs:

```text
outputs/predictions/
outputs/tables/rcc_ablation_metrics.json
```

## Example Metrics

The current smoke test runs on four deterministic mock cases. These numbers verify the pipeline behavior; they are not scientific benchmark results.

| Method | Cases | Accuracy | Evidence Support Proxy | Escalation Rate | Audit Trace Completeness |
|---|---:|---:|---:|---:|---:|
| single_agent | 4 | 0.75 | 0.00 | 0.00 | 0.00 |
| rag_only | 4 | 0.75 | 1.00 | 0.00 | 0.00 |
| homogeneous_multi_agent | 4 | 0.75 | 0.00 | 0.00 | 0.00 |
| rcc_mock_full | 4 | 0.75 | 1.00 | 0.75 | 1.00 |
| rcc_no_retrieval | 4 | 0.75 | 0.00 | 0.75 | 0.00 |
| rcc_no_guideline_verification | 4 | 0.75 | 1.00 | 0.75 | 0.00 |
| rcc_no_safety_critic | 4 | 0.75 | 1.00 | 0.00 | 0.00 |
| rcc_no_adaptive_routing | 4 | 0.75 | 1.00 | 0.75 | 1.00 |

## Repository Structure

```text
.
├── src/rcc_agents/                 # RCC prototype package
├── baselines/data/medqa/           # Small local mock/eval data
├── outputs/predictions/            # Prediction JSONL files
├── outputs/tables/                 # Metrics JSON files
├── research-wiki/                  # Lightweight research memory
├── RESEARCH_BRIEF.md               # Research direction
├── EXPERIMENT_PLAN.md              # Experiment plan
├── PAPER_PLAN.md                   # Paper outline
├── NOVELTY_CHECK.md                # Novelty positioning
├── ARIS_PROGRESS.md                # Latest progress checkpoint
└── MANIFEST.md                     # Artifact manifest
```

## Future Roadmap

Next steps:

1. Add a PubMedQA or MedQA loader for 50-100 public benchmark examples.
2. Replace `MockLLM` with one inexpensive real model backend.
3. Add better evidence-quality and hallucination scoring.
4. Wrap and compare MDAgents outputs using the same prediction schema.
5. Produce a Stage 3 experiment report with real benchmark metrics.
6. Optionally build a small UI for visualizing the agent audit trace.

## Safety and Scope

This project should only use public, de-identified datasets. It should not claim autonomous diagnosis or treatment capability. All outputs should be framed as research artifacts for clinician-in-the-loop support.
