# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- Python setup: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Install JS deps: `npm install`
- Start dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`

## Test Commands
- Python tests: `PYTHONPATH=. pytest`
- Run single test: `PYTHONPATH=. pytest src/tests/path_to_test.py::test_name`
- Generate dataset: `PYTHONPATH=. python src/generate_dataset.py`
- Validate dataset: `PYTHONPATH=. python src/validation/validate_dataset.py`

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

## Architecture Overview
The project combines synthetic customer data generation (Python) with an adaptive engagement UI system (React/TypeScript). Data generation creates realistic health personas with journey simulations, while the frontend provides personalized experiences through adaptive loading, emotional scaffolding, and progressive disclosure patterns. All components are configuration-driven and type-safe.