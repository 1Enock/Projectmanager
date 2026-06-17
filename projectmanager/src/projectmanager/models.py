from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from dateutil.parser import parse as parse_date


TASK_STATUSES = {"todo", "in_progress", "done"}


def parse_due_date(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    parsed = parse_date(value)
    return parsed.date().isoformat()


@dataclass
class User:
    id: int
    name: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(id=int(data["id"]), name=str(data["name"]))


@dataclass
class Task:
    id: int
    title: str
    status: str = "todo"
    due_date: str | None = None

    def __post_init__(self) -> None:
        if self.status not in TASK_STATUSES:
            raise ValueError(f"Invalid task status: {self.status}")
        if self.due_date is not None:
            self.due_date = parse_due_date(self.due_date)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "title": self.title, "status": self.status, "due_date": self.due_date}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            status=str(data.get("status", "todo")),
            due_date=data.get("due_date"),
        )


@dataclass
class Project:
    id: int
    name: str
    description: str = ""
    user_id: int | None = None
    tasks: list[Task] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Project":
        tasks = [Task.from_dict(item) for item in data.get("tasks", [])]
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
            user_id=data.get("user_id"),
            tasks=tasks,
        )


@dataclass
class DataSchema:
    users: list[User] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "users": [user.to_dict() for user in self.users],
            "projects": [project.to_dict() for project in self.projects],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DataSchema":
        return cls(
            users=[User.from_dict(item) for item in data.get("users", [])],
            projects=[Project.from_dict(item) for item in data.get("projects", [])],
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
