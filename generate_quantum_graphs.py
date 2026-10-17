import csv
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "results" / "tables" / "quantum_processor_ab_benchmark.csv"
OUT_DIR = ROOT / "results" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit(f"No benchmark rows found in {CSV_PATH}")

processors = ["A", "B"]
available = {row["processor"] for row in rows}
processors = [p for p in processors if p in available]

metrics = [
    ("transpile_time_ms", "Average transpilation time (ms)", "avg_transpilation_time.png"),
    ("simulation_wall_time_ms", "Average simulation wall time (ms)", "avg_simulation_time.png"),
    ("circuit_depth", "Average transpiled circuit depth", "avg_circuit_depth.png"),
    ("total_transpiled_gates", "Average number of transpiled gates", "avg_transpiled_gates.png"),
    ("cx_gate_count", "Average CX gate count", "avg_cx_gate_count.png"),
]

for column, label, filename in metrics:
    averages = []
    for processor in processors:
        values = [
            float(row[column])
            for row in rows
            if row["processor"] == processor and row.get(column, "") != ""
        ]
        averages.append(sum(values) / len(values) if values else 0)

    plt.figure(figsize=(7, 4.5))
    plt.bar(processors, averages)
    plt.ylabel(label)
    plt.title(label + " — Processor A vs B")
    plt.tight_layout()
    destination = OUT_DIR / filename
    plt.savefig(destination, dpi=200)
    plt.close()
    print(f"Saved {destination}")

print(f"Created {len(metrics)} graphs in {OUT_DIR}")
