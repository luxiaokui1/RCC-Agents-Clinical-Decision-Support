# RCC Agents Prototype

This directory contains the first runnable prototype for:

```text
Role-Conditioned Communication for Auditable Heterogeneous LLM Agents in Clinician-in-the-Loop Decision Support
```

## Current Status

The code currently provides:

- a unified prediction/audit schema
- a deterministic mock LLM for no-cost smoke tests
- a role-conditioned communication pipeline
- basic metrics
- an adapter for wrapping MDAgents output into the RCC JSONL format

## Run Mock Pipeline

From `ARIS-paper-workspace`:

```bash
python -m src.rcc_agents.run_rcc_mock --limit 1
```

Outputs:

```text
outputs/predictions/rcc_mock_medqa.jsonl
outputs/tables/rcc_mock_metrics.json
```

## Run Baseline and Ablation Suite

```bash
python -m src.rcc_agents.run_ablation_suite \
  --input baselines/data/medqa/rcc_mock_eval.jsonl
```

Outputs:

```text
outputs/predictions/<method>_medqa.jsonl
outputs/tables/rcc_ablation_metrics.json
```

## Wrap MDAgents Output

After MDAgents produces an output JSON:

```bash
python -m src.rcc_agents.wrap_mdagents_output \
  --input baselines/MDAgents/output/gpt-4o-mini_medqa_basic.json \
  --output outputs/predictions/mdagents_wrapped.jsonl
```

## Research Note

This is not model training code yet. The paper's first contribution is the communication protocol and audit/evaluation layer. Local or cloud fine-tuning can be added later as an optional extension.
