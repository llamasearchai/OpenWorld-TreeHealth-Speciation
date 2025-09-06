# Contributing to OpenWorld TSHM

Thank you for your interest in contributing to OpenWorld Tree Speciation & Health Monitoring!

## Development Setup

### Prerequisites
- Python 3.10+
- Poetry (for dependency management)
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/OpenWorld-TreeHealth&Speciation.git
   cd OpenWorld-TreeHealth&Speciation
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Development Workflow

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/openworld

# Run specific test file
pytest tests/test_specific.py
```

### Code Quality
We use several tools to maintain code quality:

```bash
# Format code
black .

# Check formatting
black --check .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Type checking
mypy src/
```

### Pre-commit Hooks
We recommend setting up pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following our coding standards
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Update documentation if needed
7. Commit your changes: `git commit -m "Describe the change succinctly"`
8. Push to your fork: `git push origin feature/your-feature`
9. Create a Pull Request

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints for all function parameters and return values
- Use descriptive variable and function names
- Keep functions small and focused
- Add docstrings to all public functions

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Add a body for complex changes

### Documentation
- Update docstrings when changing function signatures
- Add examples for complex functionality
- Keep README.md up to date

## Testing

### Unit Tests
- Write unit tests for all new functions
- Aim for >95% code coverage
- Use descriptive test names
- Test both success and error cases

### Integration Tests
- Add integration tests for new workflows
- Test end-to-end functionality
- Mock external dependencies when appropriate

### E2E Tests
- Test CLI commands as users would use them
- Verify file I/O operations
- Test complete workflows

## Architecture Guidelines

### Plugin System
- Implement new sensor plugins by extending `SensorPlugin`
- Register plugins in `pyproject.toml` entry points
- Follow the standard ingestion interface

### ML Models
- Use scikit-learn compatible models
- Include model validation and performance metrics
- Save/load models with joblib

### CLI Commands
- Use Typer for CLI argument parsing
- Provide helpful `--help` messages
- Include validation for user inputs

## Reporting Issues

When reporting bugs or requesting features:

1. Use the issue templates
2. Include Python version and OS
3. Provide steps to reproduce
4. Include error messages and stack traces
5. Suggest potential solutions if possible

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT).
