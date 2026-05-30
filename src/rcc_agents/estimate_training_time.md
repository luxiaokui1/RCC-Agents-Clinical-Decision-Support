# Training and Runtime Estimate

## Key Point

This paper does not require training a new clinical foundation model. The main contribution is a role-conditioned communication protocol, modular agent orchestration, audit tracing, and ablation evaluation.

For the first paper version, the realistic plan is:

1. Run API or local-model inference baselines.
2. Build the RCC orchestration layer.
3. Evaluate accuracy, evidence support, safety flags, abstention, cost, latency, and audit trace completeness.

## Local Machine

Detected GPU:

```text
NVIDIA GeForce RTX 4050 Laptop GPU
VRAM: about 6 GB
CUDA visible through WSL
```

### Feasible locally

- Run MDAgents API baseline: no GPU needed.
- Run mock or small local-model tests: minutes.
- Run small open-source LLMs with quantization, such as 3B-8B models: possible, but tight on 6 GB VRAM.
- Run small LoRA experiments on compact models: possible if using QLoRA and small batches.

### Not realistic locally

- Full fine-tuning 7B+ medical LLMs without aggressive quantization.
- Multi-agent local inference with several large models loaded simultaneously.
- Large benchmark sweeps over thousands of cases with local 7B+ models.

### Local time estimate

| Task | Approximate Time |
|---|---:|
| MDAgents API smoke test | 1-5 minutes, if API quota works |
| Mock RCC pipeline | seconds |
| 100-case API benchmark | 30 minutes to several hours, depending on calls per case |
| Local 3B-7B quantized inference on 100 cases | 1-6 hours |
| Small LoRA/QLoRA pilot on 3B model | 2-8 hours |
| 7B QLoRA pilot on 6 GB VRAM | possible but fragile; often 6-24 hours with careful settings |

## Cloud GPU Estimate

| Hardware | Best Use | Approximate Time |
|---|---|---:|
| T4 16 GB | small inference / tiny LoRA | 4-12 hours for pilots |
| L4 24 GB | 7B inference and QLoRA | 2-8 hours for pilots |
| RTX 4090 24 GB | fast 7B inference/QLoRA | 1-4 hours for pilots |
| A100 40/80 GB | larger sweeps and stronger local models | under 1-6 hours for many experiments |

## Recommendation

Do not start with training. Start with:

1. MDAgents as closest baseline.
2. RCC mock pipeline and wrapper.
3. Small API-based benchmark when quota is available.
4. Optional local-model substitution later if the paper needs a "no proprietary API" experiment.

Training can be framed as optional future work unless reviewers demand adaptation/fine-tuning.

