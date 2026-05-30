from __future__ import annotations

import argparse
from pathlib import Path

from .data import load_medqa_jsonl
from .io import write_json, write_jsonl
from .metrics import compute_metrics
from .pipeline import RCCPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run mock RCC pipeline on MedQA-style JSONL.")
    parser.add_argument("--input", default="baselines/data/medqa/test.jsonl")
    parser.add_argument("--output", default="outputs/predictions/rcc_mock_medqa.jsonl")
    parser.add_argument("--metrics-output", default="outputs/tables/rcc_mock_metrics.json")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    cases = load_medqa_jsonl(args.input, limit=args.limit)
    pipeline = RCCPipeline()
    predictions = [pipeline.run_case(case) for case in cases]
    write_jsonl(args.output, predictions)
    metrics = compute_metrics(predictions)
    write_json(args.metrics_output, metrics)

    print(f"Wrote predictions: {Path(args.output).resolve()}")
    print(f"Wrote metrics: {Path(args.metrics_output).resolve()}")
    print(metrics)


if __name__ == "__main__":
    main()

