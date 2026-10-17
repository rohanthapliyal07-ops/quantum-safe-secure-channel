"""Classical post-quantum secure-channel demo using liboqs-python.

The server's ML-DSA public key must be provisioned/trusted by the client out of band.
This example is educational and is not a production protocol implementation.
"""
from __future__ import annotations

import os
import struct
from dataclasses import dataclass
from typing import Any

try:
    import oqs  # provided by liboqs-python
except ImportError:  # allow tests/docs to import the module without liboqs installed
    oqs = None

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

KEM_ALGORITHM = "ML-KEM-768"
SIGNATURE_ALGORITHM = "ML-DSA-65"
PROTOCOL_LABEL = b"P1-Quantum-Safe-Secure-Channel-v1"


class SecureChannelError(RuntimeError):
    """Raised when a handshake, signature, or ciphertext check fails."""


@dataclass
class ServerIdentity:
    public_key: bytes
    secret_key: bytes


def _require_oqs() -> Any:
    if oqs is None:
        raise RuntimeError(
            "liboqs-python is not installed. Install dependencies from requirements.txt "
            "and ensure the liboqs native library is available."
        )
    return oqs


def generate_server_identity() -> ServerIdentity:
    """Create an ML-DSA-65 identity; persist/provision its public key securely."""
    oqs_mod = _require_oqs()
    with oqs_mod.Signature(SIGNATURE_ALGORITHM) as signer:
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
    return ServerIdentity(public_key=bytes(public_key), secret_key=bytes(secret_key))


def _signature_for_handshake(kem_public_key: bytes, server_name: str, client_name: str) -> bytes:
    return b"|".join((PROTOCOL_LABEL, server_name.encode(), client_name.encode(), kem_public_key))


def derive_aes_key(shared_secret: bytes, context: bytes) -> bytes:
    """Derive a 256-bit AES key with HKDF-SHA-256."""
    return HKDF(
        algorithm=hashes.SHA256(), length=32, salt=None,
        info=PROTOCOL_LABEL + b"|" + context,
    ).derive(shared_secret)


def run_handshake_and_encrypt(
    message: bytes,
    identity: ServerIdentity,
    *,
    server_name: str = "server",
    client_name: str = "client",
) -> dict[str, Any]:
    """Run one simulated client-to-server handshake and encrypt a payload.

    Signature authentication covers protocol label, identities, and the server's
    ephemeral KEM public key. The client verifies using the pre-trusted ML-DSA key.
    The KEM shared secret is independently derived by encapsulation/decapsulation.
    """
    oqs_mod = _require_oqs()
    context = (server_name + "->" + client_name).encode()

    # Server creates an ephemeral KEM keypair and signs the handshake context.
    with oqs_mod.KeyEncapsulation(KEM_ALGORITHM) as server_kem:
        kem_public_key = server_kem.generate_keypair()
        kem_secret_key = server_kem.export_secret_key()
    signed_bytes = _signature_for_handshake(bytes(kem_public_key), server_name, client_name)
    with oqs_mod.Signature(SIGNATURE_ALGORITHM, secret_key=identity.secret_key) as signer:
        signature = signer.sign(signed_bytes)

    # Client verifies the identity signature before using the KEM public key.
    with oqs_mod.Signature(SIGNATURE_ALGORITHM) as verifier:
        if not verifier.verify(signed_bytes, bytes(signature), identity.public_key):
            raise SecureChannelError("ML-DSA handshake signature verification failed")

    # Client encapsulates; server decapsulates. Shared secrets must match.
    with oqs_mod.KeyEncapsulation(KEM_ALGORITHM) as client_kem:
        ciphertext, client_shared_secret = client_kem.encap_secret(bytes(kem_public_key))
    with oqs_mod.KeyEncapsulation(KEM_ALGORITHM, secret_key=bytes(kem_secret_key)) as server_kem:
        server_shared_secret = server_kem.decap_secret(bytes(ciphertext))
    if bytes(client_shared_secret) != bytes(server_shared_secret):
        raise SecureChannelError("ML-KEM shared-secret mismatch")

    aes_key = derive_aes_key(bytes(client_shared_secret), context)
    nonce = os.urandom(12)
    aad = PROTOCOL_LABEL + b"|" + context
    encrypted = AESGCM(aes_key).encrypt(nonce, message, aad)
    # Server independently derives the key and decrypts to demonstrate interoperability.
    server_aes_key = derive_aes_key(bytes(server_shared_secret), context)
    decrypted = AESGCM(server_aes_key).decrypt(nonce, encrypted, aad)

    # Application-level transcript byte count (length prefixes included); this is
    # not a network capture and excludes transport/TLS/framing overhead.
    bytes_exchanged = sum(len(x) for x in (
        bytes(kem_public_key), bytes(signature), bytes(ciphertext),
        nonce, encrypted,
    )) + 5 * 4  # five 32-bit length prefixes in this accounting model

    return {
        "algorithm_kem": KEM_ALGORITHM,
        "algorithm_signature": SIGNATURE_ALGORITHM,
        "kdf": "HKDF-SHA-256",
        "aead": "AES-256-GCM",
        "kem_public_key": bytes(kem_public_key),
        "kem_ciphertext": bytes(ciphertext),
        "signature": bytes(signature),
        "nonce": nonce,
        "ciphertext": encrypted,
        "decrypted": decrypted,
        "correct": decrypted == message,
        "tamper_rejected": _tamper_check(aes_key, nonce, encrypted, aad),
        "bytes_exchanged_estimate": bytes_exchanged,
    }


def _tamper_check(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes) -> bool:
    altered = bytearray(ciphertext)
    if not altered:
        altered.append(1)
    else:
        altered[-1] ^= 1
    try:
        AESGCM(key).decrypt(nonce, bytes(altered), aad)
    except Exception:
        return True
    return False


def demo_round_trip(message: str = "Hello from a quantum-safe channel") -> dict[str, Any]:
    identity = generate_server_identity()
    result = run_handshake_and_encrypt(message.encode("utf-8"), identity)
    result["message"] = message
    result["decrypted_text"] = result["decrypted"].decode("utf-8")
    return result
