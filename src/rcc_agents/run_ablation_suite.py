from __future__ import annotations

import argparse
from pathlib import Path

from .data import load_medqa_jsonl
from .io import write_json, write_jsonl
from .metrics import compute_metrics
from .pipeline import RCCPipeline


DEFAULT_METHODS = [
    "single_agent",
    "rag_only",
    "homogeneous_multi_agent",
    "rcc_mock_full",
    "rcc_no_retrieval",
    "rcc_no_guideline_verification",
    "rcc_no_safety_critic",
    "rcc_no_adaptive_routing",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RCC baseline and module-ablation suite.")
    parser.add_argument("--input", default="baselines/data/medqa/test.jsonl")
    parser.add_argument("--output-dir", default="outputs/predictions")
    parser.add_argument("--metrics-output", default="outputs/tables/rcc_ablation_metrics.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--methods", nargs="*", default=DEFAULT_METHODS)
    args = parser.parse_args()

    cases = load_medqa_jsonl(args.input, limit=args.limit)
    output_dir = Path(args.output_dir)
    all_metrics: dict[str, dict[str, float | int]] = {}

    for method in args.methods:
        pipeline = RCCPipeline(method=method)
        predictions = [pipeline.run_case(case) for case in cases]
        write_jsonl(output_dir / f"{method}_medqa.jsonl", predictions)
        all_metrics[method] = compute_metrics(predictions)

    write_json(args.metrics_output, all_metrics)
    print(f"Wrote suite metrics: {Path(args.metrics_output).resolve()}")
    for method, metrics in all_metrics.items():
        print(f"{method}: {metrics}")


if __name__ == "__main__":
    main()
