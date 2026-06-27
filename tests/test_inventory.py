from cep.inventory import (
    iter_reality_gap_answer_keys,
    iter_reality_gap_case_files,
    iter_reality_gap_evidence_files,
    iter_reality_gap_example_answers,
)


def test_reality_gap_inventory_discovers_current_corpus() -> None:
    assert len(iter_reality_gap_case_files()) >= 3
    assert len(iter_reality_gap_answer_keys()) >= 3
    assert len(iter_reality_gap_example_answers()) >= 6
    assert len(iter_reality_gap_evidence_files()) >= 12
