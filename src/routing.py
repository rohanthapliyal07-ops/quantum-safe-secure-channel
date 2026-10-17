"""Legacy module placeholder.

Quantum-circuit routing is intentionally out of scope for the P1 online round.
The project benchmarks classical PQC software on Platforms A and B only.
"""

ONLINE_ROUND_SCOPE = ("Platform A", "Platform B")


def run_routing_benchmark(*args, **kwargs):
    raise NotImplementedError(
        "Quantum circuit routing is not part of the P1 online-round benchmark. "
        "Use src.benchmark.benchmark_platform('A') or ('B')."
    )
