"""Repeatable classical PQC handshake and payload benchmarks for Platforms A/B."""
from __future__ import annotations
import csv
import json
import os
import statistics
import time
import tracemalloc
from pathlib import Path
from typing import Any

from .secure_channel import generate_server_identity, run_handshake_and_encrypt

PAYLOAD_SIZES = {"1KB": 1_024, "100KB": 102_400, "10MB": 10 * 1_024 * 1_024}


def _source_code_bytes(project_root: Path) -> int:
    return sum(p.stat().st_size for p in project_root.rglob("*.py") if ".venv" not in p.parts and "__pycache__" not in p.parts)


def benchmark_platform(platform: str, repeats: int = 5, payload_sizes: dict[str, int] | None = None) -> list[dict[str, Any]]:
    if platform not in {"A", "B"}:
        raise ValueError("Online round supports Platform A and Platform B only")
    payload_sizes = payload_sizes or PAYLOAD_SIZES
    identity = generate_server_identity()  # identity setup excluded from per-handshake time
    rows: list[dict[str, Any]] = []
    root = Path(__file__).resolve().parents[1]
    code_size = _source_code_bytes(root)

    for payload_name, size in payload_sizes.items():
        payload = (b"P1 quantum-safe benchmark payload\n" * ((size // 34) + 1))[:size]
        elapsed_ms: list[float] = []
        peak_memory_bytes: list[int] = []
        byte_counts: list[int] = []
        correct = True
        tamper_rejected = True
        for _ in range(repeats):
            tracemalloc.start()
            started = time.perf_counter_ns()
            result = run_handshake_and_encrypt(payload, identity)
            elapsed = (time.perf_counter_ns() - started) / 1_000_000
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            elapsed_ms.append(elapsed)
            peak_memory_bytes.append(peak)
            byte_counts.append(result["bytes_exchanged_estimate"])
            correct = correct and result["correct"]
            tamper_rejected = tamper_rejected and result["tamper_rejected"]

        rows.append({
            "platform": platform,
            "payload": payload_name,
            "payload_bytes": size,
            "repeats": repeats,
            "handshake_encrypt_decrypt_mean_ms": round(statistics.mean(elapsed_ms), 3),
            "handshake_encrypt_decrypt_median_ms": round(statistics.median(elapsed_ms), 3),
            "python_peak_traced_memory_mean_bytes": round(statistics.mean(peak_memory_bytes)),
            "application_bytes_exchanged_estimate": round(statistics.mean(byte_counts)),
            "python_source_code_bytes": code_size,
            "correctness_passed": correct,
            "tamper_rejection_passed": tamper_rejected,
            "cpu_count_visible_to_process": os.cpu_count(),
            "memory_metric_note": "tracemalloc Python-traced peak; not total process RSS",
            "timing_note": "includes KEM keygen/encap/decap, signature, HKDF, AES-GCM and verification; excludes long-term identity keygen",
        })
    return rows


def save_results(rows: list[dict[str, Any]], output_dir: str | Path = "results/tables") -> tuple[Path, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "platform_ab_benchmark.json"
    csv_path = out / "platform_ab_benchmark.csv"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader(); writer.writerows(rows)
    return csv_path, json_path
