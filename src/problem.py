"""P1 online-round scope: classical post-quantum secure channel on A and B."""
PROJECT_TITLE = "P1: Quantum-Safe Secure Channel"
PLATFORMS = {
    "A": "Resource-rich x86-64 laptop/cloud VM; one CPU core; no hardware acceleration.",
    "B": "Same x86-64 architecture; one CPU core and a documented RAM cap.",
}
REQUIRED_ALGORITHMS = {
    "key_establishment": "ML-KEM-768 (NIST FIPS 203)",
    "authentication": "ML-DSA-65 (NIST FIPS 204)",
    "key_derivation": "HKDF-SHA-256",
    "payload_encryption": "AES-256-GCM",
}
PAYLOAD_SIZES = {"1KB": 1_024, "100KB": 102_400, "10MB": 10 * 1_024 * 1_024}
