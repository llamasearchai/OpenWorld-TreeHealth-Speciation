from __future__ import annotations
import os
from jinja2 import Template
from typing import Optional
from ..agents.forest_agent import generate_narrative
from ..utils.io import ensure_dir


HTML_TMPL = """
<!doctype html><html><head><meta charset="utf-8">
<title>OpenWorld TSHM Report</title>
<style>
body { font-family: system-ui, sans-serif; margin: 2rem; }
h1 { margin-top: 0; }
pre { background: #f6f8fa; padding: 1rem; overflow:auto; }
</style></head><body>
<h1>OpenWorld Tree Speciation & Health Monitoring</h1>
<h2>Summary</h2>
<p>{{ narrative }}</p>
<h2>Metrics</h2>
<pre>{{ metrics_json }}</pre>
</body></html>
"""


def render_report(metrics: dict, out_path: str, use_llm: str = "auto", use_agents: Optional[bool] = None) -> str:
    summary_inputs = {
        "num_trees": metrics.get("num_trees", 0),
        "avg_height": metrics.get("avg_height", 0.0),
        "species_breakdown": metrics.get("species_breakdown", {}),
        "health_index_avg": metrics.get("health_index_avg", 0.0),
    }
    narrative = generate_narrative(summary_inputs, use_llm=use_llm, use_agents=use_agents)
    tmpl = Template(HTML_TMPL)
    html = tmpl.render(narrative=narrative, metrics_json=str(metrics))
    ensure_dir(os.path.dirname(out_path))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

