import os
from openworld_tshm.provenance import ProvenanceStore


def test_provenance_log(tmp_path):
    ledger = tmp_path / "prov/ledger.jsonl"
    ps = ProvenanceStore(str(ledger))
    rec = ps.log("test_step", {"a":1}, ["in.txt"], ["out.txt"])
    assert ledger.exists()
    with open(ledger, "r", encoding="utf-8") as f:
        line = f.readline().strip()
        assert '"step": "test_step"' in line
        assert '"digest":' in line
        assert '"env":' in line

