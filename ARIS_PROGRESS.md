# ARIS Progress Checkpoint: RCC Ablation Harness

**Date:** 2026-05-30
**Workspace:** `ARIS-paper-workspace`
**Workflow stage:** Research pipeline Stage 2 implementation, moving toward Stage 3 experiment deployment

## Current State

The project has a focused research direction, novelty positioning, paper plan, experiment plan, baseline setup notes, a deterministic RCC prototype, and an initial mock result. This checkpoint extends the prototype from a single full-system run into a reproducible baseline and ablation suite.

## New Implementation Progress

Added a deterministic suite runner:

```bash
python3 -m src.rcc_agents.run_ablation_suite \
  --input baselines/data/medqa/rcc_mock_eval.jsonl
```

Implemented comparable methods:

- `single_agent`
- `rag_only`
- `homogeneous_multi_agent`
- `rcc_mock_full`
- `rcc_no_retrieval`
- `rcc_no_guideline_verification`
- `rcc_no_safety_critic`
- `rcc_no_adaptive_routing`

Generated suite metrics at:

```text
outputs/tables/rcc_ablation_metrics.json
```

## Smoke-Test Results

These are deterministic prototype results, not final LLM/API or clinical benchmark results.

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

## Next ARIS Step

Move from deterministic smoke test to a real benchmark slice:

1. Add a PubMedQA or MedQA loader for 50-100 public examples.
2. Run the same suite using one inexpensive API/local model backend.
3. Add evidence-quality scoring beyond the current proxy.
4. Wrap and compare MDAgents output with the same prediction schema.
5. Generate a Stage 3 experiment report with real benchmark metrics and representative audit traces.
