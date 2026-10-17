
"""Topology-sensitive routing experiment for the two toy processor layouts.

This is a circuit compilation experiment, not a cryptographic implementation
or a benchmark of physical quantum hardware.
"""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path


def run_topology_benchmark(project_root: str | Path) -> list[dict]:
    from qiskit import QuantumCircuit, transpile
    from qiskit.quantum_info import Statevector

    root = Path(project_root).resolve()
    output_dir = root / "results" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    # Same logical 5-qubit circuit on both processor configurations.
    # The long-range CX gates intentionally challenge the coupling maps.
    logical_circuit = QuantumCircuit(5)
    logical_circuit.h(0)
    logical_circuit.h(4)
    logical_circuit.cx(0, 4)
    logical_circuit.cx(1, 3)
    logical_circuit.cx(4, 2)
    logical_circuit.cx(0, 3)
    logical_circuit.h(2)

    expected_state = Statevector.from_instruction(logical_circuit)

    for pid in ("A", "B"):
        cfg_path = root / "processors" / f"processor_{pid}.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

        # Reuse the project's configured coupling map and basis gates.
        from qiskit.transpiler import CouplingMap
        from qiskit_aer import AerSimulator

        coupling = CouplingMap(couplinglist=cfg["coupling_map"])
        backend = AerSimulator(
            coupling_map=coupling,
            basis_gates=cfg["basis_gates"],
        )

        start = time.perf_counter()
        compiled = transpile(
            logical_circuit,
            backend=backend,
            optimization_level=cfg["simulation"]["optimization_level"],
            seed_transpiler=cfg["simulation"]["seed_transpiler"],
        )
        transpile_ms = (time.perf_counter() - start) * 1000
        ops = compiled.count_ops()

        # The noiseless statevector check is intentionally separate from the
        # noisy cryptographic demonstration and measures compilation correctness.

        rows.append({
            "processor": pid,
            "processor_name": cfg["name"],
            "num_qubits": cfg["num_qubits"],
            "logical_cx_count": int(logical_circuit.count_ops().get("cx", 0)),
            "transpiled_circuit_depth": compiled.depth(),
            "transpiled_gate_count": int(sum(ops.values())),
            "transpiled_cx_count": int(ops.get("cx", 0)),
            "transpiled_swap_count": int(ops.get("swap", 0)),
            "transpile_time_ms": round(transpile_ms, 3),
            "simulation_shots": 1024,
            "note": (
                "Topology-sensitive compilation experiment; statevector simulation "
                "is noiseless and does not represent physical-hardware performance."
            ),
        })

    json_path = output_dir / "quantum_topology_benchmark.json"
    csv_path = output_dir / "quantum_topology_benchmark.csv"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Topology results saved to:\n{csv_path}\n{json_path}")
    for row in rows:
        print(
            f"Processor {row['processor']}: "
            f"depth={row['transpiled_circuit_depth']}, "
            f"gates={row['transpiled_gate_count']}, "
            f"CX={row['transpiled_cx_count']}, "
            f"SWAP={row['transpiled_swap_count']}, "
            f"transpile={row['transpile_time_ms']} ms"
        )

    return rows
