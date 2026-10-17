"""Simple plot generation for Platform A/B benchmark CSV/JSON results."""
from __future__ import annotations
import json
from pathlib import Path


def plot_benchmarks(input_json: str | Path = "results/tables/platform_ab_benchmark.json", output_dir: str | Path = "results/figures") -> list[Path]:
    import matplotlib.pyplot as plt
    rows = json.loads(Path(input_json).read_text(encoding="utf-8"))
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    generated = []
    for metric, ylabel, filename in [
        ("handshake_encrypt_decrypt_mean_ms", "Mean end-to-end time (ms)", "platform_ab_time.png"),
        ("python_peak_traced_memory_mean_bytes", "Mean Python-traced peak memory (bytes)", "platform_ab_memory.png"),
    ]:
        labels = [f"{r['platform']} · {r['payload']}" for r in rows]
        values = [r[metric] for r in rows]
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(labels, values)
        ax.set_ylabel(ylabel); ax.set_xlabel("Platform and payload")
        ax.tick_params(axis="x", labelrotation=25)
        fig.tight_layout()
        path = out / filename; fig.savefig(path, dpi=160); plt.close(fig)
        generated.append(path)
    return generated
