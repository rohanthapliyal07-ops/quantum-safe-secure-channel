# P1: Quantum-Safe Secure Channel — Online Round Report

## 1. Scope

This project implements a classical-software post-quantum secure-channel demonstration. It benchmarks **Platform A and Platform B only**, as required for the online round. Platforms C and D and quantum-circuit experiments are out of scope.

## 2. Design

The handshake uses ML-KEM-768 (FIPS 203) to establish a shared secret. The server authenticates its ephemeral KEM public key and handshake context using ML-DSA-65 (FIPS 204). The client verifies the signature against a trusted server public key before using the KEM key. HKDF-SHA-256 derives a 256-bit symmetric key, and AES-256-GCM encrypts/authenticates the payload.

## 3. Man-in-the-middle risk

ML-KEM by itself does not authenticate a peer: an active attacker could substitute their own KEM public key. ML-DSA mitigates this risk by signing the ephemeral key and peer/context identifiers. This protection depends on the client already trusting the correct ML-DSA public key and verifying the signature over the complete relevant context. The included demonstration uses a provisioned identity key, but it is not a full certificate or network protocol.

## 4. Platforms

| Platform | Configuration | Status |
|---|---|---|
| A | x86-64, one CPU core, no hardware acceleration | Run on baseline host and record environment |
| B | Same x86-64 architecture, one CPU core, 512 MiB RAM cap by default | Enforce and document the cap before collecting results |

If the organizers provide a different RAM limit, their value supersedes the default in `processors/processor_B.json`.

## 5. Benchmark method

Payload sizes are 1 KB, 100 KB, and 10 MB. For each payload, run multiple repetitions and record mean/median end-to-end time, Python-traced peak memory, estimated application bytes exchanged, Python source code size, correctness, and tamper rejection. Per-iteration time includes ephemeral KEM key generation, encapsulation/decapsulation, ML-DSA signing/verification, HKDF, and AES-GCM; long-term identity generation is excluded.

**No measured values are included in this template.** Run `python main.py --benchmark --repeats 10` on the target host(s), then use the generated CSV/JSON as the results table. Do not present estimates as measurements. `tracemalloc` does not measure all native allocations or total process RSS; explain this limitation and collect process RSS separately if required.

## 6. Results

Populate the table from `results/tables/platform_ab_benchmark.csv` after running the benchmark:

| Platform | Payload | Mean time (ms) | Median time (ms) | Python peak traced memory (bytes) | Estimated bytes exchanged | Correct | Tamper rejected |
|---|---:|---:|---:|---:|---:|---|---|
| A | 1 KB | — | — | — | — | — | — |
| A | 100 KB | — | — | — | — | — | — |
| A | 10 MB | — | — | — | — | — | — |
| B | 1 KB | — | — | — | — | — | — |
| B | 100 KB | — | — | — | — | — | — |
| B | 10 MB | — | — | — | — | — | — |

## 7. Discussion to complete after measurement

Explain differences observed between A and B, including CPU scheduling, memory pressure, native-library behavior, payload size, and measurement variance. State whether the RAM limit was actually enforced. Report software versions, CPU model, OS/kernel, repetitions, and command used. Avoid claiming a difference caused by RAM alone unless the experiment controls other variables.

## 8. Reproduction

```bash
python -m pip install -r requirements.txt
python main.py --check
python -m unittest discover -s tests -v
python main.py --demo
python main.py --benchmark --repeats 10
```

See `docs/REFERENCE_AND_ASSUMPTIONS.md` for assumptions and security limitations.


## Quantum processor simulation extension

This repository additionally simulates a fixed, educational two-bit reversible XOR circuit on Processor A (5-qubit linear) and Processor B (9-qubit heavy-hex-inspired) using Qiskit Aer. It records transpiled circuit depth, gate counts, CX/SWAP counts, noisy measurement distributions, transpilation time, and host simulation time. These values characterize the configured simulator runs only; they are not physical quantum hardware measurements. The XOR circuit is not cryptographically secure and does not implement ML-KEM, ML-DSA, or AES. Those post-quantum secure-channel operations remain classical in this project.
