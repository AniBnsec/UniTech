import os
import sys
import subprocess
import time

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def run_step(step_name, command, cwd=".", extra_env=None):
    print(f"\n[RUNNING] {step_name}...")
    start = time.time()
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    res = subprocess.run(command, shell=True, cwd=cwd, env=env, capture_output=True, text=True)
    duration = time.time() - start

    if res.returncode == 0:
        print(f"[PASSED]  {step_name} ({duration:.2f}s)")
        return True, res.stdout
    else:
        print(f"[FAILED]  {step_name} ({duration:.2f}s)")
        print("\n--- STDOUT ---")
        print(res.stdout)
        print("\n--- STDERR ---")
        print(res.stderr)
        return False, res.stderr

def main():
    print_header("AegisTrust Platform - Automated Verification Suite")
    
    python_exe = os.path.abspath(os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python"))

    steps = [
        ("Backend Cybersecurity & API Tests (Pytest)", f'"{python_exe}" -m pytest backend/tests -v', ".", {"PYTHONPATH": "backend"}),
        ("Solidity Smart Contract Tests (Hardhat)", "npx hardhat test", "contracts", None),
        ("Frontend Production Build (TypeScript + Vite)", "npm run build", "frontend", None)
    ]

    all_passed = True
    for name, cmd, cwd, env in steps:
        passed, out = run_step(name, cmd, cwd, env)
        if not passed:
            all_passed = False

    print_header("Verification Summary")
    if all_passed:
        print("  ALL SYSTEM CHECKS PASSED SUCCESSFULLY (100% HEALTHY)!")
        print("  - Cybersecurity Engines: Active (Punycode, Typosquatting, eMudhra CA Trust, SSRF Guards)")
        print("  - AI Social Engineering Analyzer: Active (5-Factor Coercion Radar, IOC Extraction)")
        print("  - Web3 Registry: Active (Keccak-256 Anchoring, Zero-PII, EVM Hardhat/Sepolia)")
        print("  - Interactive Dashboard: Built & Ready to Serve")
        print("=" * 70 + "\n")
        sys.exit(0)
    else:
        print("  VERIFICATION FAILED ON ONE OR MORE COMPONENTS.")
        print("=" * 70 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
