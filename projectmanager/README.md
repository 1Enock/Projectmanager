# Project Manager CLI

A Python command-line application to manage users, projects, and tasks with local persistence.

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
projectmanager user add
projectmanager user list
projectmanager project add --name "Website" --description "Launch site" --owner u0001
projectmanager project list
projectmanager project search u0001
projectmanager task add --project p0001 --title "Wireframe" --description "Create wireframes" --assigned-user u0001 --due-date 2026-12-31
projectmanager task list --project p0001
projectmanager task complete t0001
```

## Persistence

Data is stored in a JSON file named `.projectmanager_data.json` in the current working directory.

## Quick Start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. (Optional) Install the package in editable mode:

```bash
python -m pip install -e .
```

4. Use the CLI from your project directory. Example:

```bash
python -m projectmanager user add
python -m projectmanager user list
python -m projectmanager project add --name "Website" --description "Launch site" --owner u0001
python -m projectmanager project list
```

5. Load the sample data into your working directory (copy the sample file):

```bash
cp data/sample_project_data.json .projectmanager_data.json
```

6. Run tests:

```bash
pytest -q
```

