# Technical Project Report: Quantum-Safe Secure Channel

**Project:** Quantum-Safe Secure Channel  
**Author:** Rohan Thapliyal  
**GitHub Repository:** https://github.com/rohanthapliyal07-ops/quantum-safe-secure-channel  
**Project Type:** Post-Quantum Cryptography and Quantum-Circuit Benchmarking  
**Implementation Language:** Python

---

## Abstract

The development of quantum computing has motivated research into cryptographic algorithms designed to remain secure against adversaries with access to sufficiently capable quantum computers. Traditional public-key cryptographic systems may be vulnerable to future quantum attacks, making post-quantum cryptography an important area of research.

This project implements an educational quantum-safe secure-channel demonstration using standardized post-quantum cryptographic algorithms. ML-KEM-768 is used for shared-secret establishment, ML-DSA-65 authenticates the handshake context, HKDF-SHA-256 derives a symmetric encryption key, and AES-256-GCM provides authenticated message encryption.

The project also investigates the performance characteristics of two configured platforms, Platform A and Platform B, through classical post-quantum cryptography benchmarks and toy quantum-circuit simulations. The implementation includes automated tests, benchmark datasets, visualizations, and technical documentation.

The secure-channel demonstration validates a simulated handshake and message round trip within a single Python process. The quantum-circuit experiments evaluate selected simulation and circuit metrics rather than demonstrating the security of the protocol against a real quantum computer.

**Keywords:** Post-quantum cryptography, ML-KEM-768, ML-DSA-65, AES-256-GCM, HKDF, secure messaging, quantum-circuit simulation, performance benchmarking.

---

## 1. Introduction

Cryptography is essential for protecting digital communications, authenticating identities, and maintaining data confidentiality and integrity. Many widely deployed public-key cryptographic systems rely on mathematical problems that are believed to be difficult for classical computers.

A sufficiently capable fault-tolerant quantum computer could threaten certain established public-key cryptographic schemes. Post-quantum cryptography addresses this challenge by developing algorithms designed to resist known attacks from both classical and quantum-capable adversaries.

NIST has standardized ML-KEM in FIPS 203 and ML-DSA in FIPS 204. These algorithms provide standardized mechanisms for establishing shared secrets and generating digital signatures, respectively.

This project explores how these mechanisms can be combined with symmetric authenticated encryption to demonstrate a simplified secure messaging workflow. It also studies the performance of configured classical and simulated quantum-processing platforms.

### 1.1 Problem Statement

The project addresses two related questions:

1. How can post-quantum cryptographic primitives be combined into a simplified authenticated message-encryption workflow?
2. How can selected performance characteristics of classical cryptographic implementations and simulated quantum circuits be measured and compared across two configured platforms?

### 1.2 Objectives

The primary objectives are:

- Implement a simulated secure-channel workflow using standardized post-quantum algorithms.
- Use ML-KEM-768 to establish a shared secret.
- Use ML-DSA-65 to authenticate the handshake context.
- Derive an AES-256 encryption key using HKDF-SHA-256.
- Encrypt and decrypt messages using AES-256-GCM.
- Demonstrate rejection of modified ciphertext.
- Benchmark the configured classical platforms A and B.
- Simulate toy quantum encryption/decryption circuits for 5-qubit and 9-qubit configurations.
- Store benchmark results in structured CSV and JSON files.
- Generate plots for performance comparison.
- Validate selected components through automated tests.

---

## 2. Scope of the Project

The project has two main components.

### 2.1 Classical Post-Quantum Secure Channel

The first component demonstrates a cryptographic workflow involving:

- Server identity generation.
- Ephemeral ML-KEM key generation.
- ML-DSA signature generation and verification.
- Shared-secret encapsulation and decapsulation.
- Symmetric key derivation.
- Authenticated encryption and decryption.
- Ciphertext tamper detection.

The client and server operations are simulated within one Python process. The project does not implement a complete network transport or a production-ready secure-channel protocol.

### 2.2 Quantum-Circuit Benchmarking

The second component simulates toy quantum encryption/decryption circuits using the configured Platform A and Platform B processor models.

The quantum-circuit benchmark code evaluates selected characteristics such as:

- Circuit depth.
- Controlled-NOT gate counts.
- Transpiled gate counts.
- Transpilation time.
- Simulation time.
- Other metrics supported by the implemented benchmark modules.

The results are useful for comparing the configured experiments. They should not be interpreted as measurements of real quantum hardware or as evidence of cryptographic security against quantum attacks.

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main implementation language |
| liboqs-python | Python interface for post-quantum cryptographic algorithms |
| liboqs | Native cryptographic implementation dependency |
| ML-KEM-768 | Shared-secret establishment |
| ML-DSA-65 | Handshake signature authentication |
| HKDF-SHA-256 | Symmetric key derivation |
| AES-256-GCM | Authenticated message encryption |
| Qiskit-related tooling | Quantum-circuit benchmarking and simulation |
| pytest | Test execution |
| unittest | Automated test framework |
| Matplotlib or project-configured plotting tools | Benchmark visualization |
| Git and GitHub | Version control and source-code hosting |

Exact runtime and native-library requirements depend on the installed dependencies and operating system.

---

## 4. System Architecture

The implementation is organized into a secure-channel component, benchmarking modules, processor configurations, result storage, visualization code, and automated tests.

### 4.1 Secure-Channel Architecture

The message workflow follows this sequence:

1. Generate or provision the server's ML-DSA-65 identity.
2. Generate an ephemeral ML-KEM-768 keypair.
3. Construct a signed handshake context containing the protocol label, identity labels, and ephemeral KEM public key.
4. Sign the context using the server's ML-DSA secret key.
5. Verify the signature using the trusted server public key.
6. Encapsulate a shared secret using the ephemeral KEM public key.
7. Decapsulate the KEM ciphertext using the corresponding secret key.
8. Check that the simulated client and server obtain matching shared secrets.
9. Derive a 256-bit AES key using HKDF-SHA-256.
10. Encrypt the message with AES-256-GCM.
11. Decrypt the ciphertext and verify that the original message is recovered.
12. Modify a ciphertext for the tamper-detection demonstration and check whether authenticated decryption rejects it.

### 4.2 Cryptographic Components

#### ML-KEM-768

ML-KEM-768 is the module-lattice-based key-encapsulation mechanism standardized in NIST FIPS 203.

In this implementation, the server creates an ephemeral KEM keypair. The client encapsulates a shared secret using the public key, and the server decapsulates the resulting ciphertext.

The shared secrets are compared in the demonstration to confirm that both sides derive the same value.

#### ML-DSA-65

ML-DSA-65 is the module-lattice-based digital signature algorithm standardized in NIST FIPS 204.

The server signs the handshake context. The client verifies the signature using a previously trusted server public key.

This provides authentication of the signed handshake data, assuming the public key is genuinely trusted and the algorithm implementation behaves correctly.

The client name in the current implementation is a context label. It does not establish a separately authenticated client identity.

#### HKDF-SHA-256

HKDF derives a symmetric key from the KEM shared secret using SHA-256.

The implementation derives a 32-byte key, corresponding to the key length required for AES-256. The protocol label and session context are incorporated into the HKDF information field.

#### AES-256-GCM

AES-GCM provides authenticated encryption with associated data.

The implementation encrypts the message using a 12-byte random nonce and authenticates protocol context through associated data. During decryption, authentication failure causes the operation to reject modified ciphertext or invalid authentication data.

Nonce uniqueness under a given key is essential for safe AES-GCM use.

---

## 5. Implementation Details

The main implementation is located in `src/secure_channel.py`.

### 5.1 Server Identity

The function `generate_server_identity()` creates an ML-DSA-65 keypair.

The resulting public key must be distributed to the client through a trusted provisioning mechanism in a real deployment. The current demo passes the identity object directly to the handshake function.

### 5.2 Handshake Authentication

The function `_signature_for_handshake()` constructs the data to be signed using:

- A protocol-version label.
- A server identity label.
- A client identity label.
- The ephemeral KEM public key.

The server signs this context using ML-DSA-65. The simulated client verifies the signature before proceeding to KEM encapsulation.

### 5.3 Shared-Secret Establishment

The function `run_handshake_and_encrypt()` creates an ephemeral KEM keypair, performs encapsulation and decapsulation, and compares the resulting shared secrets.

If signature verification or shared-secret consistency checks fail, the function raises a `SecureChannelError`.

### 5.4 Key Derivation and Message Encryption

After establishing the shared secret, the implementation derives an AES key through `derive_aes_key()`.

AES-GCM encrypts the supplied message. The simulated server derives the same key independently and decrypts the ciphertext.

The result contains the original and decrypted data, the algorithms used, cryptographic outputs, a tamper-detection result, and an application-level communication-size estimate.

### 5.5 Tamper Detection

The function `_tamper_check()` modifies one bit of the ciphertext and attempts authenticated decryption.

If decryption raises an exception, the modified ciphertext is considered rejected.

This tests ciphertext integrity for the demonstration. It does not constitute a complete test of all protocol attacks, malformed handshakes, or replay scenarios.

---

## 6. Experimental Setup

The project defines two platform configurations: Platform A and Platform B.

The quantum-circuit simulations use configured 5-qubit and 9-qubit processor models. The actual properties of each configuration should be taken from the corresponding JSON configuration files and benchmark implementation.

### 6.1 Payload Sizes

The project defines the following payload sizes:

| Payload label | Size in bytes |
|---|---:|
| 1 KB | 1,024 |
| 100 KB | 102,400 |
| 10 MB | 10,485,760 |

These sizes allow the benchmark workflow to investigate how message size affects the metrics collected by the implementation.

### 6.2 Benchmark Repetitions

The command-line interface supports a configurable repetition count. The default is five repetitions per payload, where applicable.

Repeated measurements can help characterize variability, although a rigorous performance study should also control machine load, software versions, warm-up effects, and experimental conditions.

### 6.3 Result Storage

The project retains benchmark data in CSV and JSON formats under `results/tables/`.

Visualization outputs are stored under `results/figures/`. The exact metrics and interpretation should be confirmed against the corresponding benchmark source code and recorded data.

---

## 7. Benchmark Methodology

### 7.1 Classical PQC Benchmarks

The classical benchmark workflow compares the configured Platforms A and B.

The `--benchmark` command executes the classical post-quantum benchmarking workflow. The exact operations and reported metrics are defined by the implementation in `src/benchmark.py` and its supporting modules.

Results should be analyzed by platform and payload size. Measurements should be reported with units, repetition counts, and a description of the test environment.

### 7.2 Quantum-Circuit Benchmarks

The `--quantum-benchmark` command runs the toy quantum encryption/decryption circuit benchmark workflow.

The available result artifacts include:

- `results/tables/quantum_processor_ab_benchmark.csv`
- `results/tables/quantum_processor_ab_benchmark.json`
- `results/tables/quantum_topology_benchmark.csv`
- `results/tables/quantum_topology_benchmark.json`

The available figures include circuit depth, controlled-NOT gate counts, simulation time, transpilation time, and transpiled gate counts.

These measurements characterize the implemented simulation and transpilation workflow. They do not directly predict future quantum hardware performance.

### 7.3 Reproducibility

The benchmark workflows can be executed through the command-line interface. The project retains data and visualizations for inspection.

For reproducible comparisons, the Python environment, dependency versions, processor configuration, repetition count, and relevant machine details should be documented alongside the numerical results.

---

## 8. Results and Analysis

The repository includes previously generated benchmark tables and figures. Numerical conclusions must be drawn from those recorded results rather than assumed in advance.

### 8.1 Classical Platform Comparison

The classical benchmark data is stored in:

- `results/tables/platform_ab_benchmark.csv`
- `results/tables/platform_ab_benchmark.json`

The data can be used to compare the recorded metrics for Platforms A and B across the configured workloads.

A final quantitative analysis should report the measured values, units, repetition count, and observed differences. No claim that one platform is faster or more efficient should be made without checking the actual measurements.

### 8.2 Quantum Processor Comparison

The quantum processor benchmark results are stored in the quantum processor and topology tables.

The corresponding figures provide visual comparisons of selected circuit and simulation metrics.

Circuit depth and gate counts can describe aspects of circuit complexity. Transpilation and simulation times describe the software execution environment and should not be confused with physical quantum computation time.

### 8.3 Interpretation

The two benchmark categories address different questions.

Classical PQC benchmarks evaluate the measured performance of the implemented cryptographic or platform workflows. Quantum-circuit benchmarks evaluate selected properties of toy circuits and their simulated execution.

The two categories should not be combined into a direct comparison of cryptographic security. In particular, the quantum-circuit results do not demonstrate that the implemented secure channel has been attacked or proven secure against a quantum adversary.

### 8.4 Quantitative Results Table

Complete the following table using the actual recorded measurements before submitting a final quantitative report.

| Metric | Platform A | Platform B | Units |
|---|---:|---:|---|
| Classical benchmark measurement | From recorded data | From recorded data | As defined by benchmark |
| Circuit depth | From recorded data | From recorded data | Gates/depth units |
| Controlled-NOT gate count | From recorded data | From recorded data | Gates |
| Transpilation time | From recorded data | From recorded data | As recorded |
| Simulation time | From recorded data | From recorded data | As recorded |

Only include metrics that are actually available and comparable in the corresponding result files.

---

## 9. Testing and Validation

The project includes automated tests in `tests/test_project.py`.

The test suite covers several aspects of the implementation.

### 9.1 Configuration Tests

The tests check:

- That the declared platform scope contains Platforms A and B.
- That the required algorithms are declared.
- That the configured payload sizes match the expected values.

### 9.2 Cryptographic Utility Tests

The tests verify that:

- HKDF derives a 32-byte key.
- AES-GCM can encrypt and decrypt a test message.
- Modified ciphertext is rejected by the tamper-check helper.

### 9.3 Statistical Utility Tests

The tests verify selected behaviors of the standard-error and percentage-change functions.

### 9.4 Integration Test

When `liboqs` is available, the full post-quantum handshake integration test exercises the message round trip and checks the recovered message and tamper-detection result.

The integration test is skipped when `oqs` cannot be imported. Therefore, test reports must distinguish passed tests from skipped tests.

### 9.5 Test Commands

Run the test suite using:

```bash
python -m pytest -v
```

Alternatively:

```bash
python -m unittest discover -s tests -v
```

Successful execution alone does not establish that every security property has been tested. The test output should be retained and reviewed when preparing the final submission.

---

## 10. Security Analysis

### 10.1 Confidentiality

AES-256-GCM encrypts the payload using a key derived from the shared KEM secret. Under the assumptions of the selected algorithms and correct key/nonce handling, the encrypted payload is intended to remain confidential.

### 10.2 Authentication

ML-DSA-65 authenticates the signed handshake context. This authentication depends on the client trusting the correct server public key.

The current implementation does not provide a complete identity-provisioning infrastructure.

### 10.3 Integrity

AES-GCM authenticates encrypted data and associated data. The tamper-check helper demonstrates rejection of a modified ciphertext.

### 10.4 Post-Quantum Cryptography

ML-KEM-768 and ML-DSA-65 are standardized post-quantum algorithms. Their use provides a post-quantum-oriented foundation for the demo, but overall protocol security depends on the complete implementation and its assumptions.

### 10.5 Secret Management

The implementation exports the ephemeral KEM secret key into Python-managed memory. Python does not guarantee secure erasure of immutable byte strings, so the demo does not provide strong guarantees for secret-key memory lifecycle management.

### 10.6 Protocol Limitations

The implementation does not provide a complete network protocol. It does not implement all features expected of a production secure channel, such as a fully specified transport protocol, replay protection, session lifecycle management, and a comprehensive identity-verification system.

The project should therefore be treated as an educational demonstration rather than a system for protecting real sensitive communications.

---

## 11. Limitations

The current project has the following limitations:

1. The secure-channel workflow simulates client and server operations in one Python process.
2. Server public-key provisioning is assumed rather than implemented as a complete trust infrastructure.
3. Client identity labels are not equivalent to cryptographically authenticated client identities.
4. The implementation has not been independently security-audited.
5. Python-managed secret-key memory is not guaranteed to be securely erased.
6. The quantum-circuit experiments use toy circuits and simulated execution.
7. Benchmark conclusions depend on the configured platforms, implementation, environment, and repetitions.
8. Previously generated benchmark outputs should be checked against their source code and experimental assumptions before numerical claims are published.

These limitations define the project's educational and experimental scope.

---

## 12. Future Work

Potential extensions include:

- Implementing a real client/server transport.
- Formalizing handshake transcript construction and identity binding.
- Adding replay-protection and session-management mechanisms.
- Improving secret-key lifecycle management.
- Adding negative tests for invalid signatures and malformed handshakes.
- Expanding integration tests for failure cases.
- Recording dependency versions and execution-environment metadata.
- Improving benchmark reproducibility and statistical analysis.
- Extending circuit experiments with documented configurations and clearly defined metrics.
- Conducting an independent security review before considering production deployment.

These items are potential future directions and are not claims about features already implemented.

---

## 13. Conclusion

This project demonstrates an educational combination of standardized post-quantum cryptographic primitives and symmetric authenticated encryption.

The secure-channel component combines ML-KEM-768 shared-secret establishment, ML-DSA-65 handshake authentication, HKDF-SHA-256 key derivation, and AES-256-GCM message encryption. It includes a simulated handshake, message round trip, shared-secret consistency check, and ciphertext tamper-detection demonstration.

The project also provides classical platform benchmarking and toy quantum-circuit simulation for two configured platforms. Its benchmark datasets and visualizations support further investigation of the selected performance metrics.

The primary contribution is an integrated educational prototype that brings post-quantum cryptography, authenticated messaging, automated testing, and quantum-circuit benchmarking together in one repository.

The results should be interpreted within the documented experimental scope. The implementation demonstrates cryptographic operations and simulation workflows, not a production-ready network protocol or a proof of security against real quantum computers.

---

## 14. References

1. National Institute of Standards and Technology (NIST). *FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM).*  
   https://csrc.nist.gov/pubs/fips/203/final

2. National Institute of Standards and Technology (NIST). *FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA).*  
   https://csrc.nist.gov/pubs/fips/204/final

3. Open Quantum Safe. *liboqs.*  
   https://github.com/open-quantum-safe/liboqs

4. Open Quantum Safe. *liboqs-python.*  
   https://github.com/open-quantum-safe/liboqs-python

5. Python Cryptographic Authority. *cryptography Documentation.*  
   https://cryptography.io/

6. National Institute of Standards and Technology (NIST). *FIPS 197: Advanced Encryption Standard (AES).*  
   https://csrc.nist.gov/pubs/fips/197/final

---

## Project Repository

**GitHub:** https://github.com/rohanthapliyal07-ops/quantum-safe-secure-channel

**Author:** Rohan Thapliyal

*This report documents the educational implementation and experimental scope of the Quantum-Safe Secure Channel project.*
