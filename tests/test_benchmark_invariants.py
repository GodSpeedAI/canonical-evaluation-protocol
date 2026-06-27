from cep.conformance.benchmark_invariants import run_benchmark_anti_collapse


def test_every_family_catches_its_collapses() -> None:
    results = run_benchmark_anti_collapse()

    assert results, "No benchmark invariants discovered"
    # Every family's invalid example must be caught and valid example must pass.
    assert all(r.ok for r in results), [r for r in results if not r.ok]


def test_invariants_cover_all_three_families() -> None:
    families = {r.family for r in run_benchmark_anti_collapse()}

    assert families == {"AuthorityBench", "SettlementBench", "CapabilityBench"}
