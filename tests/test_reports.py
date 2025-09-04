from openworld_tshm.reports.generate import render_report


def test_render_report(tmp_path):
    metrics = {"num_trees": 5, "avg_height": 12.3}
    out = tmp_path / "r.html"
    path = render_report(metrics, out_path=str(out), use_llm="fallback")
    assert out.exists()
    assert path.endswith(".html")


