# Project Manager CLI

A Python-based command-line application to manage users, projects, and tasks with local JSON persistence.

## Features

- Create and manage users, projects, and tasks
- Assign projects to users and search by assignee
- Persist data to a local JSON file
- Pretty-print tables and formatted dates using external packages
- Structured with modules, classes, and reusable components

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Usage

```bash
project-manager --help
```

Example commands:

```bash
project-manager create-user alice
project-manager create-project "Website Redesign" --description "Refresh homepage UI"
project-manager assign-project 1 --user-id 1
project-manager add-task 1 "Design mockups" --due-date 2026-07-01
project-manager list-projects
project-manager search-projects --user-id 1
```

## Data Storage

Data is saved by default to `data.json` in the working directory. Use `--store PATH` to change the file.

## Testing

```bash
python3 -m pytest
```
