# CLAUDE.md - Synth Project Guide

## Build Commands
- Python setup: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Install JS deps: `npm install`
- Start dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`

## Test Commands
- Python tests: `PYTHONPATH=. pytest`
- Run single test: `PYTHONPATH=. pytest src/tests/path_to_test.py::test_name`
- Generate dataset: `python src/generate_dataset.py`
- Validate dataset: `python src/validation/validate_dataset.py`

## Code Style
- **TypeScript**: 2-space indent, kebab-case filenames, Zod schemas, explicit typing
- **Python**: 4-space indent, snake_case, type hints, PEP8 style
- **React**: Functional components, custom hooks, early returns for loading/error states
- **Imports**: Group by standard library → third-party → local modules
- **Error handling**: Explicit validation for boundary conditions and type constraints
- **Documentation**: Docstrings for functions/classes, inline comments for complex logic

## Project Structure
- `src/` - Main source (Python and TypeScript)
- `engagement/` - React components using hooks pattern
- `data_generation/` - Core data generation logic
- `output/` - Generated datasets and reports