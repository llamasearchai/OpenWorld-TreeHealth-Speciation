# Developer Guide

- Run lint: `ruff check openworld_tshm tests`
- Type check: `mypy openworld_tshm`
- Tests: `pytest -q` (coverage ≥ 95%)
- Build: `hatch build`
- Docker: `docker build -t openworld-tshm . && docker run -p 8000:8000 openworld-tshm`

## Architecture

- CLI via Typer: `openworld_tshm/cli.py`
- ML: `openworld_tshm/ml/*`
- Point cloud: `openworld_tshm/pointcloud/*`
- GIS/Export: `openworld_tshm/gis/*`
- Plugins: `openworld_tshm/plugins/*`
- Dashboard: `openworld_tshm/dashboard/*`
- Reports: `openworld_tshm/reports/*`
- Provenance: `openworld_tshm/provenance.py`
- Schemas: `openworld_tshm/schemas.py`

