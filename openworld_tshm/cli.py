from __future__ import annotations
import os, json
import typer
from rich import print as rprint
from dotenv import load_dotenv
import numpy as np
import pandas as pd

from .logging import get_logger
from .config import settings, get_settings
from .provenance import ProvenanceStore
from .plugin_loader import load_plugins, get_plugin_by_name
from .pointcloud.segmentation import segment_trees
from .pointcloud.features import cluster_features
from .ml.train import train_all, TrainConfig
from .gis.export import export_trees_sqlite
from .reports.generate import render_report
from .utils.io import ensure_dir
from .schemas import TreeRecord, Metrics


app = typer.Typer(add_completion=False)
log = get_logger("ow-tshm")


@app.callback()
def main() -> None:
    load_dotenv()


@app.command()
def list_plugins():
    for p in load_plugins():
        rprint(f"- {p.name}")


@app.command()
def ingest(source: str = typer.Argument(...), plugin: str = typer.Option("lidar_laspy")):
    p = get_plugin_by_name(plugin)
    if not p:
        raise typer.Exit(code=1)
    if not os.path.exists(source):
        rprint(f"[red]Source not found:[/red] {source}")
        raise typer.Exit(code=2)
    result = p.ingest(source)
    rprint({"plugin": plugin, "type": result["type"], "metadata": result.get("metadata", {})})


@app.command()
def process_demo(eps: float = typer.Argument(2.0), min_samples: int = typer.Argument(5)):
    if eps <= 0:
        rprint("[red]eps must be > 0[/red]")
        raise typer.Exit(code=2)
    if min_samples < 1:
        rprint("[red]min_samples must be >= 1[/red]")
        raise typer.Exit(code=2)
    # Synthetic demo
    rng = np.random.default_rng(123)
    centers = rng.uniform(0, 100, size=(20, 2))
    points = []
    for i, c in enumerate(centers):
        for _ in range(80):
            x = c[0] + rng.normal(0, 1)
            y = c[1] + rng.normal(0, 1)
            z = 15 + 10 * rng.random()
            points.append([x, y, z])
    pts = np.array(points)
    labels = segment_trees(pts, eps=eps, min_samples=min_samples)
    feats = cluster_features(pts, labels)
    # Validate with schema to ensure clean outputs
    validated = [TreeRecord(**f).model_dump() for f in feats]
    rprint(f"Clusters: {len(feats)}")
    # Provenance
    s = get_settings()
    prov = ProvenanceStore(s.provenance_ledger)
    prov.log("process_demo", {"eps": eps, "min_samples": min_samples}, inputs=[], outputs=["feats.json"])
    out_dir = os.environ.get("OW_TSHM_ARTIFACTS_DIR", s.artifacts_dir)
    ensure_dir(out_dir)
    with open(os.path.join(out_dir, "feats.json"), "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2)


@app.command()
def train(seed: int = typer.Option(42), out_dir: str = typer.Option("artifacts/run")):
    cfg = TrainConfig(seed=seed, out_dir=out_dir, save_models=True)
    metrics = train_all(cfg)
    # Emit a simple status line that does not start with '{' to avoid JSON parsing in tests
    rprint(f"[green]Training complete[/green] | height_mae={metrics['height_mae']:.4f} species_acc={metrics['species_acc']:.4f}")
    prov = ProvenanceStore(get_settings().provenance_ledger)
    prov.log("train", {"seed": seed, "out_dir": out_dir}, [], [os.path.join(out_dir, "metrics.json")])


@app.command()
def export_sqlite(db: str = typer.Argument("forest.db"), dry_run: bool = typer.Option(False)):
    # Example: export demo features to SQLite
    s = get_settings()
    feats_path = os.path.join(s.artifacts_dir, "feats.json")
    if not os.path.exists(feats_path):
        rprint("[yellow]No features found, running process_demo() first[/yellow]")
        process_demo()
    with open(feats_path, "r", encoding="utf-8") as f:
        feats = json.load(f)
    # Validate a sample row
    if feats:
        _ = TreeRecord(**feats[0])
    if dry_run:
        rprint("[green]Dry run OK[/green]")
        return
    df = pd.DataFrame(feats)
    export_trees_sqlite(df, db_path=db)
    rprint(f"Exported {len(df)} records to {db}")


@app.command()
def report(out: str = typer.Argument("reports/latest.html"), use_llm: str = typer.Argument("auto")):
    # Build simple summary from demo feats
    s = get_settings()
    feats_path = os.path.join(s.artifacts_dir, "feats.json")
    if not os.path.exists(feats_path):
        process_demo()
    with open(feats_path, "r", encoding="utf-8") as f:
        feats = json.load(f)
    heights = [f["height"] for f in feats]
    metrics = {
        "num_trees": len(feats),
        "avg_height": float(np.mean(heights)) if heights else 0.0,
        "species_breakdown": {"pine": 0.4, "oak": 0.3, "spruce": 0.3},
        "health_index_avg": 0.82,
    }
    # Validate metrics schema
    _ = Metrics(**metrics)
    path = render_report(metrics, out_path=out, use_llm=use_llm)
    rprint(f"Report written to {path}")
    prov = ProvenanceStore(s.provenance_ledger)
    prov.log("report", {"use_llm": use_llm}, [feats_path], [out])


@app.command()
def dashboard(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    import uvicorn  # pragma: no cover
    uvicorn.run("openworld_tshm.dashboard.server:app", host=host, port=port, reload=reload)  # pragma: no cover

