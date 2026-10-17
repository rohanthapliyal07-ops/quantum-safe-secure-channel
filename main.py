"""P1 online-round runner: classical PQC demo and Platform A/B benchmarks."""
from __future__ import annotations
import argparse
import json
from pathlib import Path



def main() -> int:
    parser = argparse.ArgumentParser(description="P1 Quantum-Safe Secure Channel (online round: A/B only)")
    parser.add_argument("--check", action="store_true", help="check Python dependencies and required ML-KEM/ML-DSA algorithms")
    parser.add_argument("--demo", action="store_true", help="run a single authenticated encrypted-message demo")
    parser.add_argument("--interactive-message", action="store_true", help="prompt for a message and run the demo")
    parser.add_argument("--benchmark", action="store_true", help="benchmark classical PQC Platforms A and B")
    parser.add_argument("--quantum-benchmark", action="store_true", help="simulate toy quantum encrypt/decrypt circuits on 5-qubit A and 9-qubit B")
    parser.add_argument("--all-benchmarks", action="store_true", help="run both classical PQC and quantum-circuit benchmarks")
    parser.add_argument("--platform", choices=["A", "B"], help="benchmark one platform only")
    parser.add_argument("--repeats", type=int, default=5, help="repetitions per payload (default: 5)")
    parser.add_argument("--no-plots", action="store_true", help="skip plotting benchmark results")
    args = parser.parse_args()

    if args.check:
        try:
            import cryptography
            import oqs
            kem = oqs.get_enabled_kem_mechanisms()
            sig = oqs.get_enabled_sig_mechanisms()
            missing = []
            if "ML-KEM-768" not in kem:
                missing.append("ML-KEM-768")
            if "ML-DSA-65" not in sig:
                missing.append("ML-DSA-65")
            print(f"Python: dependency imports OK; cryptography {cryptography.__version__}")
            print(f"liboqs-python: {getattr(oqs, '__version__', 'installed')}")
            print(f"ML-KEM-768 available: {'ML-KEM-768' in kem}")
            print(f"ML-DSA-65 available: {'ML-DSA-65' in sig}")
            if missing:
                print("Missing required algorithms: " + ", ".join(missing))
                return 2
            print("Environment check passed. Next run: python main.py --demo")
            return 0
        except Exception as exc:
            print("Environment check failed:", str(exc))
            print("See README.md -> Installation troubleshooting.")
            return 2

    if args.interactive_message:
        message = input("Enter a message to encrypt: ")
        from src.secure_channel import demo_round_trip
        result = demo_round_trip(message)
        print(json.dumps({k: v for k, v in result.items() if k not in {"kem_public_key", "kem_ciphertext", "signature", "nonce", "ciphertext", "decrypted"}}, indent=2))
        print("Decrypted message:", result["decrypted_text"])
        return 0
    if args.demo:
        from src.secure_channel import demo_round_trip
        result = demo_round_trip()
        print(json.dumps({k: v for k, v in result.items() if k not in {"kem_public_key", "kem_ciphertext", "signature", "nonce", "ciphertext", "decrypted"}}, indent=2))
        print("Decrypted message:", result["decrypted_text"])
        return 0

    if args.quantum_benchmark or args.all_benchmarks:
        try:
            from src.qiskit_processor_benchmark import run_quantum_benchmarks
            message = "Hi"
            run_quantum_benchmarks(Path(__file__).resolve().parent, message=message)
        except Exception as exc:
            print("Quantum benchmark failed:", str(exc))
            print("Check that qiskit and qiskit-aer are installed and processor JSON files are valid.")
            return 2
        if args.quantum_benchmark and not args.all_benchmarks and not args.benchmark and not args.platform:
            return 0

    if args.benchmark or args.platform or args.all_benchmarks:
        from src.benchmark import benchmark_platform, save_results
        from src.visualization import plot_benchmarks
        platforms = [args.platform] if args.platform else ["A", "B"]
        if args.repeats < 1:
            parser.error("--repeats must be at least 1")
        rows = []
        for platform in platforms:
            print(f"Benchmarking Platform {platform}...")
            rows.extend(benchmark_platform(platform, repeats=args.repeats))
        csv_path, json_path = save_results(rows)
        print(f"Wrote {csv_path} and {json_path}")
        if not args.no_plots:
            try:
                print("Plots:", ", ".join(map(str, plot_benchmarks(json_path))))
            except ImportError:
                print("matplotlib unavailable; skipped plots")
        return 0

    parser.print_help()
    print("\nQuick start: python main.py --check, --demo, --quantum-benchmark, or --all-benchmarks")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
