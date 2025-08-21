## Stage 02: Tooling Setup — Reproducible Project Scaffold

This repository implements a clean, reproducible Python project scaffold with isolated environments, environment-driven configuration, a verification notebook, and an initialized GitHub remote, following the Stage 02 assignment guidelines [1].

### Environment Setup
- Usage: Create a dedicated Python 3.11 environment (conda or venv) and install base packages (python-dotenv, numpy, jupyter).
- Reasoning: Isolation prevents dependency conflicts and ensures experiments are reproducible across machines.

### Project Structure
- Usage: Organize source and assets under a minimal, conventional layout:
  - data/
  - notebooks/
  - src/
  - README.md, .gitignore
- Reasoning: Consistent structure accelerates onboarding and keeps code, notebooks, and data clearly separated.

### Secrets Management (.env)
- Usage: Provide `.env.example` and copy to `.env` with:
  - API_KEY=dummy_key_123
  - DATA_DIR=./data
- Reasoning: Environment variables keep secrets and paths out of code and version control while remaining easy to configure.

### Configuration Helper (src/config.py)
- Usage: Implement load_env() to load variables from `.env` and get_key() to read environment values at runtime.
- Reasoning: Centralized configuration access reduces boilerplate and avoids hard-coded constants.

### Jupyter Verification
- Usage: Add notebooks/00_project_setup.ipynb with:
  - A short “Environment & Config Check” section,
  - Code to load `.env` and confirm the presence of `API_KEY`,
  - A simple NumPy demonstration (e.g., small array operation).
- Reasoning: Provides a quick, executable sanity check that the environment and configuration are wired correctly (“API_KEY present: True”).

### Dependency Lockfile
- Usage: Export a lockfile with `pip freeze > requirements.txt`.
- Reasoning: Captures exact versions to reproduce the environment in CI or on collaborator machines.

### Version Control & Remote
- Usage: Initialize Git, make initial commits, add a remote, and push to GitHub; ensure `.env` (and optionally `/data/`) is listed in `.gitignore`.
- Reasoning: Establishes history, enables collaboration, and protects sensitive files from being committed.

### Reproducibility & Validation
- Environment: New machine can recreate the environment from requirements.txt.
- Configuration: `.env` provides portable, non-hard-coded paths and keys; config helper reads them in code.
- Notebook: Runs top-to-bottom without errors and prints the expected checks.
- Repository: Clear initial commits with a tidy scaffold and documentation.

### Submission
- Usage: Share the GitHub repository URL per the assignment instructions. [1]
- Reasoning: Allows reviewers to verify structure, notebook execution, and version history.

### Integrity & Hygiene
- Do not commit real secrets; only dummy keys in examples.
- Keep notebooks executable from top to bottom and avoid side effects beyond the project workspace.

Reference: [1] stage02_tooling-setup_homework-sheet.pdf