# 🔐 Quantum-Safe Secure Channel

**A Post-Quantum Cryptography Project with Secure Messaging and Quantum-Circuit Benchmarks**

A Python-based educational prototype demonstrating a post-quantum secure messaging workflow using ML-KEM-768 for shared-secret establishment, ML-DSA-65 for handshake authentication, HKDF-SHA-256 for key derivation, and AES-256-GCM for authenticated message encryption.

The project also evaluates classical cryptographic-platform performance and simulates toy quantum encryption/decryption circuits for two processor configurations, Platform A and Platform B.

> **Project scope:** This is an educational prototype and benchmarking project, not a production-ready network security protocol. The quantum-circuit experiments are simulations and do not demonstrate resistance to real quantum attacks.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Cryptographic Algorithms](#-cryptographic-algorithms)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Benchmarking](#-benchmarking)
- [Results and Metrics](#-results-and-metrics)
- [Testing](#-testing)
- [Security Considerations](#-security-considerations)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [References](#-references)
- [Author](#-author)

---

## 🎯 Overview

Quantum computing presents a long-term challenge to widely used public-key cryptographic systems. Post-quantum cryptography (PQC) develops cryptographic algorithms designed to resist attacks from both classical and quantum-capable adversaries.

This project explores how standardized post-quantum cryptographic algorithms can be combined with conventional symmetric encryption to demonstrate a secure messaging workflow.

The implementation covers two main areas:

1. **Classical post-quantum secure messaging:** A simulated handshake establishes a shared secret, authenticates the server's ephemeral KEM public key, derives an encryption key, and encrypts and decrypts a message.
2. **Quantum-circuit benchmarking:** Toy quantum circuits are simulated to compare selected circuit and processor-related metrics across two configurations, Platform A and Platform B.

The project also provides benchmark data, plots, automated tests, and documentation of assumptions and experimental scope.

## ✨ Key Features

- **Post-quantum key establishment:** Uses ML-KEM-768.
- **Digital-signature authentication:** Uses ML-DSA-65 to authenticate the handshake.
- **Secure key derivation:** Derives a 256-bit AES key using HKDF-SHA-256.
- **Authenticated message encryption:** Uses AES-256-GCM.
- **Tamper detection demonstration:** Checks whether a modified ciphertext is rejected.
- **Shared-secret consistency check:** Compares the client and server shared secrets in the simulated handshake.
- **Interactive messaging demo:** Accepts a user-provided message.
- **Classical PQC benchmarks:** Evaluates Platforms A and B.
- **Quantum-circuit simulations:** Simulates toy encryption/decryption circuits for 5-qubit and 9-qubit configurations.
- **Performance analysis:** Includes benchmark tables and visualization outputs.
- **Automated testing:** Uses pytest-compatible tests built with Python's unittest framework.

## 🔑 Cryptographic Algorithms

| Component | Algorithm | Purpose |
|---|---|---|
| Key establishment | ML-KEM-768 | Establishes a shared secret |
| Handshake authentication | ML-DSA-65 | Verifies the signed handshake context |
| Key derivation | HKDF-SHA-256 | Derives a symmetric encryption key |
| Message encryption | AES-256-GCM | Encrypts and authenticates message data |
| Random nonce | 12-byte random nonce | Supplies the AES-GCM nonce for each encryption operation |

### Standards

- **ML-KEM:** NIST FIPS 203
- **ML-DSA:** NIST FIPS 204
- **AES-GCM:** Authenticated encryption with associated data
- **HKDF:** HMAC-based key derivation function

The implementation uses `liboqs-python` for post-quantum cryptographic operations and the Python `cryptography` package for symmetric encryption and key derivation.

## 🏗️ System Architecture

The secure-channel demonstration follows this simplified workflow:

```text
                 SERVER IDENTITY
                 ML-DSA-65 KEYPAIR
                        |
                        v
              Generate Ephemeral KEM
                  Keypair (Server)
                        |
                        v
             Sign Handshake Context
              Using ML-DSA-65
                        |
                        v
        +--------------------------------+
        | Client Verifies the Signature  |
        | Using the Trusted Public Key   |
        +--------------------------------+
                        |
                        v
             ML-KEM-768 Encapsulation
                 (Client Side)
                        |
                        v
             ML-KEM-768 Decapsulation
                 (Server Side)
                        |
                        v
              Shared Secret Agreement
                        |
                        v
                  HKDF-SHA-256
                        |
                        v
                 AES-256-GCM Key
                        |
                        v
              Authenticated Encryption
                        |
                        v
                Ciphertext + Nonce
                        |
                        v
              Authenticated Decryption
                        |
                        v
                 Original Message
```

### Workflow Summary

1. Generate or provision the server's ML-DSA-65 identity.
2. Generate an ephemeral ML-KEM-768 keypair for the handshake.
3. Sign the protocol context, server identity, client identity label, and ephemeral KEM public key.
4. Verify the signature using the trusted server public key.
5. Perform KEM encapsulation and decapsulation to derive matching shared secrets.
6. Derive an AES-256 key using HKDF-SHA-256.
7. Encrypt the message with AES-256-GCM.
8. Decrypt the ciphertext and verify that the recovered message matches the original.
9. Demonstrate ciphertext tamper detection by modifying the encrypted data.

**Implementation note:** The current workflow simulates both client and server operations within one Python process. It is not a deployed network protocol.

## 📂 Project Structure

```text
quantum_safe_secure_channel/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── assets/
│   └── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── REFERENCE_AND_ASSUMPTIONS.md
│
├── processors/
│   ├── platform_A.json
│   ├── platform_B.json
│   ├── processor_A.json
│   └── processor_B.json
│
├── results/
│   ├── figures/
│   └── tables/
│
├── src/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── metrics.py
│   ├── problem.py
│   ├── processors.py
│   ├── qiskit_processor_benchmark.py
│   ├── routing.py
│   ├── secure_channel.py
│   ├── topology_benchmark.py
│   └── visualization.py
│
├── tests/
│   └── test_project.py
│
├── generate_quantum_graphs.py
├── main.py
├── report.md
├── requirements.txt
├── .gitignore
└── README.md
```

### Important Directories

- `src/`: Core implementation, cryptographic workflow, benchmarking, metrics, and visualization modules.
- `tests/`: Automated project tests.
- `processors/`: Configuration files for the two processor platforms.
- `results/tables/`: Generated or retained benchmark datasets in CSV and JSON formats.
- `results/figures/`: Benchmark plots and visualizations.
- `docs/`: Technical references, assumptions, and documentation.
- `report.md`: Detailed project report.

## 💻 Requirements

- Python 3.10 or a compatible version supported by the installed dependencies
- Git
- Visual Studio Code (recommended)
- A working C/C++ build toolchain if required by native dependencies on your platform
- The dependencies listed in `requirements.txt`
- A compatible installation of `liboqs` and `liboqs-python` for the ML-KEM and ML-DSA integration

Native-library availability can depend on your operating system and Python environment.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rohanthapliyal07-ops/quantum-safe-secure-channel.git
cd quantum-safe-secure-channel
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can invoke the environment's Python executable directly instead.

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project requirements:

```bash
python -m pip install -r requirements.txt
```

Install pytest if it is not included in the requirements:

```bash
python -m pip install pytest
```

**Note:** Installing Python packages alone may not install the native `liboqs` library. Follow the `liboqs-python` installation instructions if the post-quantum integration cannot load.

## ▶️ Usage

Run commands from the project root with the virtual environment activated.

### 1. Check Dependencies and Algorithms

```bash
python main.py --check
```

Checks Python dependencies and the required ML-KEM/ML-DSA algorithms.

### 2. Run the Secure-Channel Demo

```bash
python main.py --demo
```

Runs a single authenticated encrypted-message demonstration.

### 3. Send a Custom Message

```bash
python main.py --interactive-message
```

Prompts for a message and runs the demonstration using that input.

### 4. Run Classical PQC Benchmarks

```bash
python main.py --benchmark
```

Benchmarks classical post-quantum cryptographic Platforms A and B.

### 5. Run Quantum-Circuit Benchmarks

```bash
python main.py --quantum-benchmark
```

Runs the toy quantum encryption/decryption circuit simulations for the configured 5-qubit and 9-qubit platforms.

### 6. Run All Benchmarks

```bash
python main.py --all-benchmarks
```

Runs the classical PQC and quantum-circuit benchmark workflows.

### 7. Run a Specific Platform

```bash
python main.py --benchmark --platform A
```

Or:

```bash
python main.py --benchmark --platform B
```

### 8. Control the Number of Repetitions

```bash
python main.py --all-benchmarks --repeats 2
```

This uses two repetitions per payload where the selected benchmark supports the shared repetitions option. Use more repetitions for more stable measurements.

### 9. Skip Benchmark Plot Generation

```bash
python main.py --all-benchmarks --no-plots
```

Useful when you only need to run the benchmarks without generating plots.

### Windows PowerShell Alternative

If the virtual environment is not activated, invoke Python directly:

```powershell
.\.venv\Scripts\python.exe main.py --check
.\.venv\Scripts\python.exe main.py --demo
.\.venv\Scripts\python.exe main.py --interactive-message
.\.venv\Scripts\python.exe main.py --all-benchmarks
```

## 📊 Benchmarking

The project includes two categories of experiments.

### A. Classical Post-Quantum Cryptography

The classical benchmarking workflow evaluates the configured Platforms A and B.

Depending on the benchmark implementation, the collected metrics can include:

- Execution time
- Encryption/decryption-related performance
- Payload-size effects
- Communication-size estimates
- Comparative performance between platforms

The secure-channel implementation includes an application-level byte-count estimate for selected handshake and encrypted-message fields. This is not a network packet capture and excludes transport, TLS, and other framing overhead.

### B. Quantum-Circuit Simulation

The quantum benchmarking workflow simulates toy quantum encryption/decryption circuits using the configured 5-qubit and 9-qubit processor models.

Available result files include:

- `results/tables/quantum_processor_ab_benchmark.csv`
- `results/tables/quantum_processor_ab_benchmark.json`
- `results/tables/quantum_topology_benchmark.csv`
- `results/tables/quantum_topology_benchmark.json`

Generated visualizations include:

- `results/figures/avg_circuit_depth.png`
- `results/figures/avg_cx_gate_count.png`
- `results/figures/avg_simulation_time.png`
- `results/figures/avg_transpilation_time.png`
- `results/figures/avg_transpiled_gates.png`

Additional platform comparison results are stored under `results/tables/` and `results/figures/`.

**Interpretation:** These experiments compare selected implementation and simulation metrics. They do not establish the security of the classical protocol against a quantum adversary or predict the performance of a future fault-tolerant quantum computer.

## 📈 Results and Metrics

The repository retains benchmark data and visualization outputs so the results can be inspected and reproduced.

| Result category | Location |
|---|---|
| Platform A/B benchmark data | `results/tables/platform_ab_benchmark.csv` |
| Platform A/B benchmark JSON | `results/tables/platform_ab_benchmark.json` |
| Quantum processor benchmark | `results/tables/quantum_processor_ab_benchmark.csv` |
| Quantum topology benchmark | `results/tables/quantum_topology_benchmark.csv` |
| Benchmark visualizations | `results/figures/` |
| Technical discussion | `report.md` |

The actual measurements should be interpreted in the context of the configured platforms, benchmark code, machine environment, and repetition count.

No performance figures are stated here because benchmark values should be taken directly from the recorded experiment outputs rather than estimated or invented.

## 🧪 Testing

The project includes tests implemented with Python's `unittest` framework, which can also be executed through pytest.

Run the full test suite:

```bash
python -m pytest -v
```

Alternatively:

```bash
python -m unittest discover -s tests -v
```

The current tests cover:

- Platform A/B scope
- Required algorithm declarations
- Configured payload sizes
- HKDF key derivation
- AES-GCM encryption/decryption and ciphertext tampering
- Statistical metric calculations
- The complete post-quantum handshake round trip when `liboqs` is available

**Testing note:** The full handshake integration test is skipped when `oqs` is unavailable. Review the test output to distinguish passed tests from skipped tests.

## 🛡️ Security Considerations

This project demonstrates cryptographic building blocks and a simplified handshake, but it is not a substitute for a reviewed production protocol.

Important assumptions and limitations include:

1. **Trusted server identity:** The server's ML-DSA public key must be provisioned and trusted by the client out of band.
2. **Simulated handshake:** Client and server operations execute within one process; there is no implemented network transport.
3. **Ephemeral KEM key handling:** Secret-key material is exported into Python-managed memory in the current implementation.
4. **Nonce management:** AES-GCM requires nonce uniqueness for each encryption under the same key. The current demo generates a random 12-byte nonce.
5. **Client identity:** The client name in the handshake is a context label, not proof of a cryptographically authenticated client identity.
6. **Production hardening:** Network framing, replay protection, session management, key storage, denial-of-service controls, and independent security review are outside the current scope.
7. **Quantum simulations:** Simulated circuits are experimental demonstrations, not evidence that the messaging protocol has been tested against a quantum computer.

Do not use this prototype to protect real sensitive communications without substantial additional engineering, review, and testing.

## ⚠️ Limitations

- The secure-channel demonstration is in-process rather than client/server networking.
- Server identity provisioning is assumed rather than implemented as a complete trust infrastructure.
- Quantum encryption/decryption circuits are toy simulations.
- Benchmark results depend on the configured processor models, environment, and repetition count.
- Performance measurements do not establish cryptographic security.
- The implementation is educational and has not been independently audited.

## 🚀 Future Improvements

Possible future directions include:

- Implementing a real client/server transport.
- Adding stronger handshake and transcript-binding tests.
- Implementing explicit replay protection and session management.
- Improving secret-key lifecycle management.
- Adding reproducible benchmark environment metadata.
- Extending benchmark analysis with confidence intervals and repeated trials.
- Adding CI checks for dependency installation and automated tests.
- Improving documentation of processor assumptions and experiment methodology.
- Conducting an independent security review before any production use.

## 📚 References

1. NIST, **FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM)**.  
   https://csrc.nist.gov/pubs/fips/203/final

2. NIST, **FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA)**.  
   https://csrc.nist.gov/pubs/fips/204/final

3. Open Quantum Safe, **liboqs**.  
   https://github.com/open-quantum-safe/liboqs

4. Open Quantum Safe, **liboqs-python**.  
   https://github.com/open-quantum-safe/liboqs-python

5. Python Cryptographic Authority, **cryptography documentation**.  
   https://cryptography.io/

6. NIST, **FIPS 197: Advanced Encryption Standard (AES)**.  
   https://csrc.nist.gov/pubs/fips/197/final

## 👨‍💻 Author

**Rohan Thapliyal**

GitHub: [@rohanthapliyal07-ops](https://github.com/rohanthapliyal07-ops)

Repository: [quantum-safe-secure-channel](https://github.com/rohanthapliyal07-ops/quantum-safe-secure-channel)

---

**Built as an educational exploration of post-quantum cryptography, authenticated secure messaging, and quantum-circuit benchmarking.**
