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
