# RCC Agents: Auditable Multi-Agent Clinical Decision Support Prototype

RCC Agents is a research prototype for **Role-Conditioned Communication (RCC)**, a modular multi-agent LLM framework for clinician-in-the-loop clinical decision support.

The project asks a focused research question:

> If medical LLM agents are required to communicate through role-specific, evidence-aware, risk-aware messages, can the final answer become easier to audit, safer to review, and more suitable for clinical decision-support settings?

This repository is not a medical product. It is not a diagnosis system, treatment system, or substitute for a clinician. It is an early research and engineering scaffold for studying auditable medical multi-agent workflows.

## Project Summary

Most LLM question-answering systems produce a final answer directly. Even many multi-agent systems rely on loosely structured debate or role prompts, which can make it hard to inspect what evidence was used, which module introduced risk, or why the final output should be trusted.

RCC Agents explores a different design:

- split the workflow into explicit clinical-support roles
- make each role communicate through structured messages
- require evidence where appropriate
- preserve risk flags and escalation decisions
- produce an audit trace alongside the final answer
- run ablation studies to measure what each module contributes

The current implementation is intentionally lightweight. It uses a deterministic mock LLM backend so the pipeline can be run locally without API keys or GPU resources. The main value of the current version is the system design, schema, ablation harness, and reproducible experiment outputs.

## What The System Does

Given a medical QA-style case, the system routes the case through several agent roles:

| Agent role | Responsibility |
|---|---|
| `case_context` | Summarizes the patient/question context into a structured working summary. |
| `evidence_retrieval` | Retrieves or attaches supporting evidence from benchmark context or trusted documents. |
| `clinical_reasoning` | Produces a candidate answer and reasoning path. |
| `guideline_verification` | Checks whether the candidate answer is supported by evidence or conflicts with guideline-like context. |
| `safety_critic` | Flags unsupported, unsafe, overconfident, or treatment-like recommendations. |
| `final_synthesis` | Produces the final answer with evidence, uncertainty, escalation metadata, and audit trace. |

Each agent step creates a structured `RoleMessage` containing fields such as:

```json
{
  "sender_role": "evidence_retrieval",
  "receiver_role": "clinical_reasoning",
  "message_type": "evidence_packet",
  "evidence_required": true,
  "allowed_action": "use_as_support_only",
  "uncertainty": "low",
  "risk_flags": [],
  "escalation_required": false
}
```

This makes the output more than a plain answer. It becomes a traceable record of how the answer was produced.

## What Makes It Multi-Agent

This prototype does not use a heavy multi-agent framework. Instead, it implements a research-oriented multi-agent workflow directly in Python.

The multi-agent behavior appears in four places:

1. **Role decomposition**: each module represents a different clinical-support role.
2. **Structured message passing**: modules exchange `RoleMessage` records rather than unstructured chat text.
3. **Audit trace preservation**: the final prediction includes the full sequence of agent messages.
4. **Module ablation**: individual roles can be removed to test their contribution.

The full RCC flow is:

```text
case_context
  -> clinical_reasoning

evidence_retrieval
  -> clinical_reasoning

clinical_reasoning
  -> guideline_verification

guideline_verification
  -> safety_critic

safety_critic
  -> final_synthesis
```

## Technology Stack

Current implementation:

- **Language**: Python
- **Interface**: command line
- **Data format**: JSONL and JSON
- **Agent orchestration**: custom lightweight pipeline
- **Model backend**: deterministic `MockLLM`
- **Evaluation**: custom metrics for accuracy, evidence support, escalation, and audit trace completeness
- **Research workflow**: ARIS-generated research brief, paper plan, experiment plan, progress checkpoint, and artifact manifest

The project currently does not use:

- LangGraph
- LangChain
- CrewAI
- AutoGen
- LlamaIndex
- a database
- a web UI
- real LLM API calls
- GPU training

These can be added later, but the first version keeps the core research idea small and inspectable.

## Does It Have a UI?

No. The current version is a command-line research prototype.

There is no web dashboard, chat UI, Streamlit app, or React frontend yet. The system is run through Python commands, and outputs are written to files:

```text
outputs/predictions/
outputs/tables/
```

A future UI could show:

- the input case
- each agent's message
- retrieved evidence spans
- safety flags
- escalation decisions
- the final synthesized answer
- a visual audit timeline

## Does It Have Storage?

There is no database in the current version.

The project uses file-based storage so the experiment remains easy to inspect and version-control:

| Stored item | Location |
|---|---|
| Input examples | `baselines/data/medqa/*.jsonl` |
| Prediction outputs | `outputs/predictions/*.jsonl` |
| Metrics | `outputs/tables/*.json` |
| Research progress | `ARIS_PROGRESS.md` |
| Artifact manifest | `MANIFEST.md` |
| Research notes | `research-wiki/` |

This is enough for the current prototype. If the project becomes an interactive application, a database such as PostgreSQL or SQLite could store sessions, audit traces, and evaluation runs.

## Does It Use AI?

The current repository does **not** call a real AI model yet.

It uses `MockLLM`, a deterministic stand-in that simulates the places where real AI calls will happen. This lets the pipeline, data schema, ablation runner, and metrics be tested without API keys or cost.

The AI integration points are already present conceptually:

| Current mock function | Future real AI behavior |
|---|---|
| `answer_option(case)` | LLM-based answer selection or reasoning |
| `summarize_case(case)` | LLM case summarization |
| `retrieve_evidence(case, prediction)` | RAG, benchmark-context retrieval, PubMed retrieval, or vector search |
| `verify_guideline_alignment(case, prediction)` | LLM/rule-based evidence and guideline consistency check |
| `safety_review(case, prediction)` | LLM safety critic and escalation evaluator |

The next technical milestone is to add a real backend, such as OpenAI, DeepSeek, Qwen/DashScope, or a local Hugging Face model.

## Why This Project Is Useful

This project is useful because it creates a concrete testbed for a real research question:

> In high-stakes domains, is multi-agent collaboration enough, or do agents need role-conditioned communication rules to become auditable?

The framework can help study:

- whether evidence requirements improve answer support
- whether safety critics increase useful escalation behavior
- whether guideline verification improves trace quality
- whether full RCC provides better auditability than direct answering
- how much each module contributes under ablation
- how to structure clinical-support LLM outputs for human review

It is also useful as a portfolio/research artifact because it shows:

- system decomposition
- structured data modeling
- reproducible experiment design
- baseline and ablation thinking
- careful safety framing in a healthcare AI context

## Baselines And Ablations

The experiment suite currently compares:

| Method | Meaning |
|---|---|
| `single_agent` | One direct answerer without retrieval or audit-oriented modules. |
| `rag_only` | Retrieval/evidence plus final answer, without full multi-agent workflow. |
| `homogeneous_multi_agent` | Multiple role-like steps without full RCC constraints. |
| `rcc_mock_full` | Full RCC workflow with retrieval, verification, safety, and synthesis. |
| `rcc_no_retrieval` | Full RCC with evidence retrieval removed. |
| `rcc_no_guideline_verification` | Full RCC with verification removed. |
| `rcc_no_safety_critic` | Full RCC with safety review removed. |
| `rcc_no_adaptive_routing` | Full RCC variant used to study routing/cost behavior. |

This is an ablation study: remove one module at a time and observe what changes.

## Current Status

The project currently includes:

- a research brief
- a novelty check
- a paper plan
- an experiment plan
- a deterministic RCC prototype
- a baseline and ablation suite runner
- a four-case mock evaluation set
- generated smoke-test predictions
- generated smoke-test metrics
- an ARIS progress checkpoint

Latest progress is summarized in:

```text
ARIS_PROGRESS.md
```

## Quick Start

From the repository root:

```bash
python3 -m src.rcc_agents.run_ablation_suite \
  --input baselines/data/medqa/rcc_mock_eval.jsonl
```

Outputs are written to:

```text
outputs/predictions/
outputs/tables/rcc_ablation_metrics.json
```

The mock suite is intentionally small. It verifies that the pipeline runs and that the output schema is consistent across methods.

## Example Smoke-Test Metrics

These results come from four deterministic mock cases. They are not final benchmark results.

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

Interpretation:

- Accuracy is not meaningful yet because the model is mocked and the sample size is tiny.
- Evidence support changes when retrieval is removed.
- Escalation behavior changes when safety review is removed.
- Audit completeness drops when key modules are missing.

## Repository Structure

```text
.
|-- src/rcc_agents/                 # RCC prototype package
|   |-- pipeline.py                  # Multi-agent pipeline and ablation routing
|   |-- mock_llm.py                  # Deterministic mock LLM backend
|   |-- schemas.py                   # Case, evidence, message, prediction schemas
|   |-- metrics.py                   # Evaluation metrics
|   |-- run_ablation_suite.py        # Baseline and ablation runner
|   `-- run_rcc_mock.py              # Single mock RCC run
|-- baselines/data/medqa/            # Small local mock/eval data
|-- outputs/predictions/             # Prediction JSONL files
|-- outputs/tables/                  # Metrics JSON files
|-- research-wiki/                   # Lightweight research memory
|-- RESEARCH_BRIEF.md                # Research direction
|-- NOVELTY_CHECK.md                 # Novelty positioning
|-- EXPERIMENT_PLAN.md               # Experiment plan
|-- PAPER_PLAN.md                    # Paper outline
|-- ARIS_PROGRESS.md                 # Latest progress checkpoint
|-- MANIFEST.md                      # Artifact manifest
`-- README.md
```

## Relationship To ARIS

This project was developed inside an ARIS/Codex research workflow. ARIS helped organize:

- research framing
- novelty positioning
- paper planning
- experiment planning
- implementation checkpoints
- result logging

The repository itself is a standalone research prototype. It does not require ARIS to run the current Python scripts.

## Future Roadmap

Near-term:

1. Add a PubMedQA or MedQA loader for 50-100 public benchmark examples.
2. Replace `MockLLM` with one real model backend.
3. Add evidence-quality and hallucination scoring beyond the current proxy.
4. Compare against MDAgents using a shared prediction schema.
5. Generate a Stage 3 experiment report with real benchmark metrics.

Medium-term:

1. Add a simple UI for visualizing agent traces.
2. Add persistent storage for sessions and experiment runs.
3. Add configurable agent backends for different model providers.
4. Add cost and latency tracking per module.
5. Expand evaluation to PubMedQA, MedQA, and MedMCQA.

Long-term:

1. Turn the protocol into a reusable framework for high-stakes multi-agent auditing.
2. Study heterogeneous model councils, where different providers/models play different roles.
3. Produce a full workshop or conference paper with real-data experiments.

## Safety And Scope

This project should only use public, de-identified datasets. It should avoid:

- autonomous diagnosis claims
- treatment recommendation claims
- real patient data without authorization
- fabricated citations
- claims that the system replaces clinicians

All outputs should be framed as research artifacts for clinician-in-the-loop support.

## One-Sentence Resume Summary

Built a Python research prototype for auditable clinical multi-agent LLM workflows, implementing role-conditioned communication, structured audit traces, baseline/ablation evaluation, mock benchmark outputs, and a roadmap toward real PubMedQA/MedQA experiments.
