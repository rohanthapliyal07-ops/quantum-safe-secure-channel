"""Educational quantum-circuit XOR encryption/decryption on processor A and B.

This is a small reversible circuit demonstration, NOT ML-KEM, ML-DSA, AES, or secure cryptography.
"""
from __future__ import annotations
import csv, json, statistics, time
from pathlib import Path
from typing import Any


def _load_processor(root: Path, processor_id: str):
    from qiskit.transpiler import CouplingMap
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
    cfg = json.loads((root / "processors" / f"processor_{processor_id}.json").read_text(encoding="utf-8"))
    noise_cfg = cfg["noise"]
    noise = NoiseModel()
    p1 = float(noise_cfg["single_qubit_depolarizing_probability"])
    p2 = float(noise_cfg["two_qubit_depolarizing_probability"])
    pr = float(noise_cfg["readout_error_probability"])
    if p1: noise.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["x", "sx"])
    if p2: noise.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    if pr:
        noise.add_all_qubit_readout_error(ReadoutError([[1-pr, pr], [pr, 1-pr]]))
    coupling = CouplingMap(couplinglist=cfg["coupling_map"])
    backend = AerSimulator(noise_model=noise, coupling_map=coupling, basis_gates=cfg["basis_gates"])
    return cfg, backend


def _make_circuit(num_qubits: int, value: int, key: int, decrypt: bool = False):
    """Two-bit plaintext XOR two-bit key; fixed four active qubits on A and B."""
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(num_qubits, 2)
    # Encode two data bits on q0,q1 and two key bits on q2,q3. Other processor
    # qubits remain available for routing but are not part of the logical message.
    for bit in range(2):
        if (value >> bit) & 1: qc.x(bit)
        if (key >> bit) & 1: qc.x(2 + bit)
    # XOR encryption and XOR decryption are the same reversible operation.
    # Apply the key-controlled CNOTs twice only in decrypt mode, to demonstrate
    # the inverse circuit on the encrypted value.
    if decrypt:
        for bit in range(2): qc.cx(2 + bit, bit)
    else:
        for bit in range(2): qc.cx(2 + bit, bit)
    qc.measure([0, 1], [0, 1])
    return qc


def _counts_to_int(counts: dict[str, int]) -> tuple[int, float]:
    total=sum(counts.values())
    if not total: return 0, 0.0
    best=max(counts, key=counts.get)
    # Qiskit two-bit classical display string is c1c0.
    return int(best.replace(" ", ""), 2), counts[best]/total


def run_quantum_benchmarks(project_root: str | Path, *, shots: int | None = None, message: str = "Hi") -> list[dict[str, Any]]:
    """Run the same 2-bit reversible XOR demonstration on both processor simulations.

    UTF-8 bytes are split into 2-bit chunks so the report records the whole input,
    but this remains an insecure toy transformation and not a real cryptographic protocol.
    """
    from qiskit import transpile
    root=Path(project_root).resolve()
    shot_count=int(shots or 4096)
    raw=message.encode("utf-8") or b"\x00"
    chunks=[]
    for byte_index, byte in enumerate(raw):
        for shift in (6,4,2,0):
            chunks.append((byte_index, shift, (byte >> shift) & 0b11))
    key=0b01
    rows=[]
    for pid in ("A", "B"):
        cfg, backend=_load_processor(root,pid)
        for chunk_index, (byte_index, shift, plain_chunk) in enumerate(chunks):
            cipher_chunk=plain_chunk ^ key
            for operation, logical_value, expected in (("encrypt", plain_chunk, cipher_chunk), ("decrypt", cipher_chunk, plain_chunk)):
                qc=_make_circuit(cfg["num_qubits"], logical_value, key, decrypt=(operation=="decrypt"))
                t0=time.perf_counter()
                compiled=transpile(qc, backend=backend, optimization_level=cfg["simulation"]["optimization_level"], seed_transpiler=cfg["simulation"]["seed_transpiler"])
                transpile_ms=(time.perf_counter()-t0)*1000
                t1=time.perf_counter()
                result=backend.run(compiled, shots=shot_count, seed_simulator=42).result()
                sim_ms=(time.perf_counter()-t1)*1000
                counts=result.get_counts()
                observed, majority_fraction=_counts_to_int(counts)
                rows.append({
                    "processor":pid,"processor_name":cfg["name"],"num_qubits":cfg["num_qubits"],
                    "message_utf8":message,"byte_index":byte_index,"two_bit_chunk_index":chunk_index,
                    "bit_shift_in_byte":shift,"operation":operation,"input_value_2bit":logical_value,"key_2bit":key,
                    "expected_output_2bit":expected,"most_common_output_2bit":observed,
                    "most_common_output_matches_expected":observed==expected,
                    "most_common_outcome_fraction":round(majority_fraction,6),"shots":shot_count,
                    "transpile_time_ms":round(transpile_ms,3),"simulation_wall_time_ms":round(sim_ms,3),
                    "circuit_depth":compiled.depth(),"total_transpiled_gates":sum(compiled.count_ops().values()),
                    "cx_gate_count":int(compiled.count_ops().get("cx",0)),"swap_gate_count":int(compiled.count_ops().get("swap",0)),
                    "measurement_counts":json.dumps(counts,sort_keys=True),
                    "noise_model":json.dumps(cfg["noise"],sort_keys=True),
                    "note":"Educational 2-bit XOR chunk only; not ML-KEM/ML-DSA/AES. Runtime is host simulator time, not quantum hardware latency."
                })
    out=root/"results"/"tables"; out.mkdir(parents=True,exist_ok=True)
    csv_path=out/"quantum_processor_ab_benchmark.csv"; json_path=out/"quantum_processor_ab_benchmark.json"
    json_path.write_text(json.dumps(rows,indent=2),encoding="utf-8")
    with csv_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"Quantum benchmark results: {csv_path} and {json_path}")
    for pid in ("A", "B"):
        subset=[r for r in rows if r["processor"]==pid]
        print(f"Processor {pid}: {len(subset)} chunk-operation simulations; majority-output matches {sum(r['most_common_output_matches_expected'] for r in subset)}/{len(subset)}")
    return rows
