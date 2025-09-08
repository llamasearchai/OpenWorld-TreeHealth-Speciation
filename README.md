## OpenWorld Tree Health & Speciation API

Production-ready FastAPI service for tree health assessment, species classification, and AI-assisted diagnosis using OpenAI.

### Features
- Health check endpoint
- Rule-based species classification
- OpenAI-powered diagnosis endpoint (Responses API)
- Config via environment variables
- Tests with pytest and httpx
- Dockerized with multi-stage build
- Makefile for common tasks

### Quickstart
1. Create and populate `.env` from `.env.example`.
2. Install and run tests:
```bash
python -m venv .venv && . .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
pytest -q
```
3. Run the API:
```bash
uvicorn openworld_treehealth.app:app --reload
```

### Docker
```bash
make docker-build
make docker-run
```

### Environment
Provide `OPENAI_API_KEY` to enable the diagnosis endpoint. Without a key, the endpoint returns a 503 error.

### Author
Nik Jois <nikjois@llamasearch.ai>

<p align="center">
  <img src="./OpenWorld-Trees.png" alt="OpenWorld TSHM Logo" width="640" />
</p>

# OpenWorld Tree Speciation & Health Monitoring

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://img.shields.io/badge/coverage-93.95%25-green.svg)](https://github.com/llamasearchai/openworld-tshm)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue.svg)](https://github.com/llamasearchai/openworld-tshm/actions)

A comprehensive forest analytics platform that integrates drone/LiDAR imagery, multispectral data, and field measurements to assess tree speciation, height, and overall health for optimized harvest and afforestation planning.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Features

### Core Capabilities

- **Point Cloud Processing**: LiDAR data ingestion (LAS/LAZ via `laspy`) with CSV fallback support
- **Tree Segmentation**: DBSCAN-based clustering for individual tree crown identification
- **Canopy Height Model**: CHM computation with percentile-based ground filtering
- **Machine Learning Models**:
  - Species classification (Random Forest, >75% accuracy)
  - Height estimation (Random Forest, <7.5m MAE)
- **Geospatial Analysis**: GIS-enabled decision support with export capabilities
- **Data Provenance**: Cryptographic signing of all pipeline steps with SHA256 hashing

### User Interfaces

- **Command Line Interface**: Full-featured CLI with comprehensive commands
- **Web Dashboard**: FastAPI-based dashboard with Leaflet map integration
- **Report Generation**: HTML reports with LLM integration for narrative insights
- **Data Publishing**: Datasette integration for interactive data exploration

### Advanced Features

- **Plugin Architecture**: Extensible sensor plugin system for new modalities
- **LLM Integration**: OpenAI Agents SDK and local LLM support via `llm` framework
- **Observability**: Prometheus metrics endpoint with request tracking
- **Containerization**: Multi-stage Docker builds with health checks
- **Security**: Input validation, size guards, and secure configuration management

## Installation

### Prerequisites

- Python 3.10 or higher
- Git
- (Optional) Docker for containerized deployment

### Install from Source

```bash
# Clone the repository
git clone https://github.com/llamasearchai/openworld-tshm.git
cd openworld-tshm

# Install with development dependencies
pip install -e ".[dev]"

# Or with uv (recommended)
uv venv && uv pip install -e ".[dev]"
```

### Optional Dependencies

```bash
# For geospatial processing
pip install -e ".[geo]"

# For sensor data processing
pip install -e ".[sensors]"

# For LLM integrations
pip install -e ".[llm]"
```

## Quick Start

1. **Install and verify**:
   ```bash
   pip install -e ".[dev]"
   openworld-tshm --help
   ```

2. **Run the test suite**:
   ```bash
   pytest -q
   ```

3. **Launch the dashboard**:
   ```bash
   openworld-tshm dashboard --host 0.0.0.0 --port 8000
   ```

4. **Process sample data**:
   ```bash
   # Generate synthetic forest data
   openworld-tshm process-demo --eps 2.0 --min-samples 5

   # Train machine learning models
   openworld-tshm train --seed 42 --out-dir artifacts/run_001

   # Generate analysis report
   openworld-tshm report --out reports/latest.html --use-llm fallback
   ```

## Usage

### Command Line Interface

The CLI provides comprehensive commands for all operations:

```bash
# List available sensor plugins
openworld-tshm list-plugins

# Ingest LiDAR data
openworld-tshm ingest --plugin lidar_laspy data/points.las

# Process field survey data
openworld-tshm ingest --plugin field_csv data/tree_measurements.csv

# Run end-to-end analysis
openworld-tshm process-demo --eps 2.0 --min-samples 5

# Train ML models with reproducible results
openworld-tshm train --seed 42 --out-dir artifacts/run_$(date +%s)

# Export results to SQLite database
openworld-tshm export-sqlite --db forest.db

# Generate HTML analysis report
openworld-tshm report --out reports/latest.html --use-llm fallback

# Launch interactive dashboard
openworld-tshm dashboard --host 0.0.0.0 --port 8000
```

### Web Dashboard

Access the dashboard at `http://localhost:8000` to:
- Visualize tree clusters on interactive maps
- Explore analysis results
- Monitor system metrics via `/metrics` endpoint
- View generated reports

### Data Publishing

Publish analysis results for interactive exploration:

```bash
# Export to SQLite and serve with Datasette
openworld-tshm export-sqlite --db forest.db
datasette serve forest.db -m datasette.yml
```

### OpenAI Agents Integration

To generate narrative insights with OpenAI’s modern Agents/Responses API (with automatic fallback):

```bash
pip install -e ".[llm]"
export OPENAI_API_KEY=sk-...
# Optional overrides
export OPENAI_MODEL=gpt-4o-mini
export OW_TSHM_USE_OAI_AGENTS=true  # prefer Agents/Responses API

# Generate a report using OpenAI
openworld-tshm report --out reports/latest.html --use-llm openai

# Override per-run to disable Agents and use chat completions
openworld-tshm report --out reports/latest.html --use-llm openai --no-use-agents

# Or explicitly enable Agents per-run
openworld-tshm report --out reports/latest.html --use-llm openai --use-agents
```

Behavior:
- With `--use-llm openai` and a valid key, the agent prefers the Responses API when enabled, otherwise uses Chat Completions.
- With `--use-llm auto`, it tries OpenAI if configured; otherwise, a deterministic fallback narrative is used.

## Keywords

- Forestry analytics, LiDAR, CHM, ML, GIS, FastAPI, Datasette, Plugins, Provenance, OpenAI, Agents

## Architecture

### System Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Processing      │───▶│   Outputs       │
│                 │    │  Pipeline        │    │                 │
│ • LiDAR (LAS)   │    │                  │    │ • SQLite DB     │
│ • Multispectral │    │ • Ingestion      │    │ • HTML Reports  │
│ • Field Surveys │    │ • Segmentation   │    │ • GeoJSON       │
│ • CSV Files     │    │ • ML Models      │    │ • API Endpoints │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Components

- **Plugin System**: Extensible architecture for new sensor types
- **ML Pipeline**: Scikit-learn based models for species and height prediction
- **Provenance System**: Cryptographic tracking of all data transformations
- **Web Services**: FastAPI backend with Leaflet frontend
- **Data Flow**: Point clouds → Segmentation → Features → ML → Reports

### Plugin Architecture

Add new sensor plugins by implementing the `SensorPlugin` interface:

```python
from openworld_tshm.plugins.base import SensorPlugin

class MySensorPlugin(SensorPlugin):
    name = "my_sensor"

    def ingest(self, source: str, **kwargs) -> dict:
        # Your ingestion logic here
        return {
            "type": "pointcloud",  # or "raster" or "field"
            "data": processed_data,
            "metadata": {"source": source, "format": "custom"}
        }
```

Register the plugin in `pyproject.toml`:

```toml
[project.entry-points."openworld_tshm.plugins"]
my_sensor = "my_package.my_module:MySensorPlugin"
```

## Development

### Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=openworld_tshm

# Run specific test categories
pytest tests/test_ml_thresholds.py  # ML model validation
pytest tests/integration/           # Integration tests
pytest tests/e2e/                   # End-to-end tests
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy openworld_tshm

# Build documentation
mkdocs build
```

### Docker Development

```bash
# Build development image
docker build -t openworld-tshm:dev .

# Run tests in container
docker run --rm openworld-tshm:dev pytest -q

# Run dashboard in container
docker run --rm -p 8000:8000 openworld-tshm:dev
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up your development environment
- Running tests and quality checks
- Submitting pull requests
- Code style guidelines

### Development Setup

```bash
# Clone and install
git clone https://github.com/llamasearchai/openworld-tshm.git
cd openworld-tshm
pip install -e ".[dev]"

# Run tests
pytest

# Start developing!
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Nik Jois — nikjois@llamasearch.ai

## Citation

If you use this software in your research, please cite:

```bibtex
@software{openworld_tshm,
  title = {OpenWorld Tree Speciation & Health Monitoring},
  author = {Jois, Nik},
  url = {https://github.com/llamasearchai/openworld-tshm},
  year = {2025}
}
```

## Acknowledgments

- Built with Python 3.10+ and modern data science libraries
- Uses FastAPI for web services and Leaflet for mapping
- Inspired by open-source geospatial and forestry research tools
- Thanks to the scientific Python community for excellent libraries
