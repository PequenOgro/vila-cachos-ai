"""
Unified CLI Runner for the Vila Cachos AI Opaque-Box 4-Tier E2E Test Suite.

Usage:
  python tests/e2e/run_e2e.py --dry-run
  python tests/e2e/run_e2e.py --tier all
  python tests/e2e/run_e2e.py --tier 1
  python tests/e2e/run_e2e.py --verify-build-splits
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.e2e.infra import (  # noqa: E402
    CSV_PATH,
    FIXTURE_HAIR_TIPO2,
    FIXTURE_HAIR_TIPO3,
    FIXTURE_HAIR_TIPO4,
    TOTEM_UI_DIR,
    CsvBackupGuard,
    ReadOnlySuiteEnv,
    find_browser_executable,
    sha256_file,
    stop_all_managed_processes,
)

TIER_MODULES: Dict[str, str] = {
    "1": "tests.e2e.test_tier1_core",
    "2": "tests.e2e.test_tier2_boundaries",
    "3": "tests.e2e.test_tier3_pairwise",
    "4": "tests.e2e.test_tier4_scenarios",
}


def iter_test_cases(suite: unittest.TestSuite) -> List[unittest.TestCase]:
    cases: List[unittest.TestCase] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            cases.extend(iter_test_cases(item))
        else:
            cases.append(item)
    return cases


def load_tier_suites(tier: str) -> Dict[str, unittest.TestSuite]:
    loader = unittest.TestLoader()
    keys = ["1", "2", "3", "4"] if tier == "all" else [tier]
    return {k: loader.loadTestsFromName(TIER_MODULES[k]) for k in keys}


def verify_build_splits() -> int:
    assets_dir = TOTEM_UI_DIR / ".output" / "public" / "assets"
    if not assets_dir.exists():
        print(f"[ERROR] Build assets directory not found: {assets_dir}")
        return 1

    js_files = sorted(assets_dir.glob("*.js"))
    webp_files = sorted(assets_dir.glob("*.webp"))
    png_files = sorted(assets_dir.glob("*.png"))
    total_js_kb = sum(p.stat().st_size for p in js_files) / 1024.0
    total_webp_kb = sum(p.stat().st_size for p in webp_files) / 1024.0

    print("=== Frontend Build Split & Asset Verification (read-only) ===")
    print(f"Assets dir: {assets_dir}")
    print(f"JS chunks ({len(js_files)}, total {total_js_kb:.2f} KB):")
    for jf in js_files:
        print(f"  - {jf.name}: {jf.stat().st_size / 1024.0:.2f} KB")
    print(f"WebP assets: {len(webp_files)} ({total_webp_kb:.2f} KB) | Legacy PNG assets: {len(png_files)}")

    ok = True
    if len(js_files) < 3:
        print("[FAIL] Expected >= 3 split JS chunks (/admin + lazy tabs/modals + /)")
        ok = False
    if len(webp_files) < 25:
        print(f"[FAIL] Expected >= 25 optimized .webp product/hero assets, found {len(webp_files)}")
        ok = False
    return 0 if ok else 1


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vila Cachos AI 4-Tier E2E Test Runner")
    parser.add_argument(
        "--tier",
        choices=["1", "2", "3", "4", "all"],
        default="all",
        help="Tier to execute (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover tests, verify fixtures/browser/CSV hash, and exit without running",
    )
    parser.add_argument(
        "--verify-build-splits",
        action="store_true",
        help="Read-only check on totem-ui/.output/public/assets/ for multi-chunk JS splitting & WebP assets",
    )
    args = parser.parse_args(argv)

    if args.verify_build_splits:
        rc_split = verify_build_splits()
        if rc_split != 0 and args.dry_run:
            return rc_split
        if not args.dry_run and rc_split != 0:
            return rc_split
        if args.verify_build_splits and len(sys.argv) == 2:
            return rc_split

    suites = load_tier_suites(args.tier)
    counts = {k: len(iter_test_cases(s)) for k, s in suites.items()}
    total_tests = sum(counts.values())
    csv_sha_before = sha256_file(CSV_PATH)

    print("=== Vila Cachos AI — 4-Tier Opaque-Box E2E Suite ===")
    for k, c in counts.items():
        print(f"  Tier {k} ({TIER_MODULES[k]}): {c} tests")
    print(f"  Total discovered: {total_tests} tests")
    print(f"  CSV SHA-256 before: {csv_sha_before}")

    if args.dry_run:
        browser_exe = find_browser_executable()
        for f in (FIXTURE_HAIR_TIPO2, FIXTURE_HAIR_TIPO3, FIXTURE_HAIR_TIPO4, CSV_PATH):
            if not f.exists():
                print(f"[FAIL] Missing required fixture: {f}")
                return 1
        print(f"  Headless CDP browser: {browser_exe}")
        if args.tier == "all":
            assert counts["1"] >= 40, f"Tier 1 < 40: {counts['1']}"
            assert counts["2"] >= 41, f"Tier 2 < 41: {counts['2']}"
            assert counts["3"] >= 8, f"Tier 3 < 8: {counts['3']}"
            assert counts["4"] >= 6, f"Tier 4 < 6: {counts['4']}"
            assert total_tests >= 95, f"Total < 95: {total_tests}"
        print("[DRY-RUN OK] All fixtures, browser binary, and tier thresholds verified.")
        return 0

    master_suite = unittest.TestSuite(list(suites.values()))
    guard = CsvBackupGuard.acquire_global()
    result = None
    try:
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(master_suite)
    finally:
        # Strict teardown order: stop all browser/vite/uvicorn trees BEFORE restoring CSV
        ReadOnlySuiteEnv.shutdown()
        stop_all_managed_processes()
        guard.exit()

    csv_sha_after = sha256_file(CSV_PATH)
    print(f"  CSV SHA-256 before: {csv_sha_before}")
    print(f"  CSV SHA-256 after : {csv_sha_after}")
    if csv_sha_before != csv_sha_after:
        print("[FAIL] CSV SHA-256 changed after E2E teardown!")
        return 1

    return 0 if (result is not None and result.wasSuccessful()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
