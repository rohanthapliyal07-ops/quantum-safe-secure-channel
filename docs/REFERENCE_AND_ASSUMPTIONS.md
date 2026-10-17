# References, scope, and assumptions

## Online-round scope

This implementation follows the supplied P1 framework note: the cryptographic algorithms execute as classical software. Online round covers only:

- Platform A: x86-64 laptop/cloud VM, single CPU core, no hardware acceleration.
- Platform B: same architecture, one CPU core and limited RAM representative of a deployed backend.

Platforms C and D are offline-round scope and are intentionally not implemented here. The old `src/routing.py` filename is retained for repository compatibility but no quantum-circuit experiment is run or used in the results.

## Algorithms

- ML-KEM-768 — NIST FIPS 203, key establishment.
- ML-DSA-65 — NIST FIPS 204, peer/server authentication.
- HKDF-SHA-256 — derive an AES-256 key from the KEM shared secret.
- AES-256-GCM — payload confidentiality and integrity.
- Implementation uses liboqs-python bindings for PQC and the `cryptography` package for HKDF/AES-GCM. Exact library versions must be recorded with the final benchmark.

## Handshake model

The demo models one authenticated server-to-client handshake and client-to-server encrypted payload: the server produces an ephemeral ML-KEM public key, signs the protocol label and identities plus that key with its provisioned ML-DSA key, the client verifies against a pre-trusted public key, and ML-KEM encapsulation/decapsulation creates a matching shared secret. Both sides derive the same symmetric key. The signature prevents undetected substitution of the ephemeral KEM public key only when the signing public key is correctly trusted and the signed context is checked.

This is a demonstrator, not a complete wire protocol. It does not implement a network socket, certificate infrastructure, replay protection, key rotation, or a production-grade peer identity system. `bytes_exchanged_estimate` is a model of application-level bytes, not a packet capture.

## Benchmark assumptions

- Payload sizes: 1,024 bytes, 102,400 bytes, 10,485,760 bytes.
- Identity key generation is outside the per-handshake timing because the server identity is long-lived; ephemeral KEM key generation is included.
- Timing includes handshake crypto and payload encrypt/decrypt to provide an end-to-end per-message measure.
- Memory is `tracemalloc` peak Python allocation. It does not include all native liboqs allocations and must not be described as total process memory.
- Code size is the sum of repository Python source file sizes, not compiled executable size or installed dependency size.
- Platform B defaults to a 512 MiB memory cap as a project choice unless the organizer's official configuration specifies otherwise. Actual enforcement must be confirmed and recorded.
- No benchmark numbers are prefilled. Results must be generated on the actual test environment.

## Security caveats

Do not write new cryptographic primitives. Trust the ML-DSA public key out of band. In production, use an established protocol/library design and undergo independent security review. Avoid exposing detailed cryptographic error differences over a network. The demo's tamper test verifies AES-GCM integrity failure; it is not a complete threat-model test suite.
