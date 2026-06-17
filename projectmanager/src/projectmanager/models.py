from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from dateutil.parser import parse as parse_date


@dataclass
class User:
    user_id: str
    name: str
    email: str

    def to_dict(self) -> dict[str, str]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(
            user_id=str(data["user_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
        )


@dataclass
class Task:
    task_id: str
    title: str
    description: str
    project_id: str
    assigned_user_id: str | None = None
    due_date: str | None = None
    status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "project_id": self.project_id,
            "assigned_user_id": self.assigned_user_id,
            "due_date": self.due_date,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return cls(
            task_id=str(data["task_id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            project_id=str(data["project_id"]),
            assigned_user_id=(str(data["assigned_user_id"]) if data.get("assigned_user_id") else None),
            due_date=(str(data["due_date"]) if data.get("due_date") else None),
            status=str(data.get("status", "pending")),
        )

    def due_date_object(self) -> datetime | None:
        if not self.due_date:
            return None
        return parse_date(self.due_date)


@dataclass
class Project:
    project_id: str
    name: str
    description: str
    owner_user_ids: list[str] = field(default_factory=list)
    task_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "owner_user_ids": self.owner_user_ids,
            "task_ids": self.task_ids,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        return cls(
            project_id=str(data["project_id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
            owner_user_ids=[str(uid) for uid in data.get("owner_user_ids", [])],
            task_ids=[str(tid) for tid in data.get("task_ids", [])],
        )


class ProjectTracker:
    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self.users: dict[str, User] = {}
        self.projects: dict[str, Project] = {}
        self.tasks: dict[str, Task] = {}
        self.next_user_id = 1
        self.next_project_id = 1
        self.next_task_id = 1
        self._load()

    def _load(self) -> None:
        storage = Storage(self.data_path)
        raw = storage.load()
        self.users = {
            uid: User.from_dict(item)
            for uid, item in raw.get("users", {}).items()
        }
        self.projects = {
            pid: Project.from_dict(item)
            for pid, item in raw.get("projects", {}).items()
        }
        self.tasks = {
            tid: Task.from_dict(item)
            for tid, item in raw.get("tasks", {}).items()
        }
        self.next_user_id = int(raw.get("next_user_id", 1))
        self.next_project_id = int(raw.get("next_project_id", 1))
        self.next_task_id = int(raw.get("next_task_id", 1))

    def _save(self) -> None:
        storage = Storage(self.data_path)
        storage.save({
            "users": {uid: user.to_dict() for uid, user in self.users.items()},
            "projects": {pid: project.to_dict() for pid, project in self.projects.items()},
            "tasks": {tid: task.to_dict() for tid, task in self.tasks.items()},
            "next_user_id": self.next_user_id,
            "next_project_id": self.next_project_id,
            "next_task_id": self.next_task_id,
        })

    def _next_id(self, prefix: str, counter: int) -> str:
        return f"{prefix}{counter:04d}"

    def create_user(self, name: str, email: str) -> User:
        user_id = self._next_id("u", self.next_user_id)
        self.next_user_id += 1
        user = User(user_id=user_id, name=name, email=email)
        self.users[user_id] = user
        self._save()
        return user

    def list_users(self) -> list[User]:
        return list(self.users.values())

    def get_user(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def create_project(self, name: str, description: str, owner_user_ids: list[str] | None = None) -> Project:
        owner_user_ids = owner_user_ids or []
        project_id = self._next_id("p", self.next_project_id)
        self.next_project_id += 1
        project = Project(project_id=project_id, name=name, description=description, owner_user_ids=owner_user_ids)
        self.projects[project_id] = project
        self._save()
        return project

    def get_project(self, project_id: str) -> Project | None:
        return self.projects.get(project_id)

    def list_projects(self) -> list[Project]:
        return list(self.projects.values())

    def assign_project_to_user(self, project_id: str, user_id: str) -> Project | None:
        project = self.get_project(project_id)
        if project and user_id not in project.owner_user_ids:
            project.owner_user_ids.append(user_id)
            self._save()
        return project

    def search_projects_by_user(self, user_id: str) -> list[Project]:
        return [project for project in self.projects.values() if user_id in project.owner_user_ids]

    def create_task(
        self,
        title: str,
        description: str,
        project_id: str,
        assigned_user_id: str | None = None,
        due_date: str | None = None,
    ) -> Task:
        task_id = self._next_id("t", self.next_task_id)
        self.next_task_id += 1
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            project_id=project_id,
            assigned_user_id=assigned_user_id,
            due_date=due_date,
        )
        self.tasks[task_id] = task
        project = self.get_project(project_id)
        if project:
            project.task_ids.append(task_id)
        self._save()
        return task

    def list_tasks(self, project_id: str | None = None) -> list[Task]:
        if project_id:
            return [task for task in self.tasks.values() if task.project_id == project_id]
        return list(self.tasks.values())

    def get_task(self, task_id: str) -> Task | None:
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: str, status: str) -> Task | None:
        task = self.get_task(task_id)
        if task:
            task.status = status
            self._save()
        return task

    def assign_task(self, task_id: str, user_id: str) -> Task | None:
        task = self.get_task(task_id)
        if task:
            task.assigned_user_id = user_id
            self._save()
        return task

    def delete_user(self, user_id: str) -> bool:
        if user_id not in self.users:
            return False
        del self.users[user_id]
        for project in self.projects.values():
            project.owner_user_ids = [uid for uid in project.owner_user_ids if uid != user_id]
        for task in self.tasks.values():
            if task.assigned_user_id == user_id:
                task.assigned_user_id = None
        self._save()
        return True

    def delete_project(self, project_id: str) -> bool:
        project = self.projects.pop(project_id, None)
        if not project:
            return False
        for task_id in project.task_ids:
            self.tasks.pop(task_id, None)
        self._save()
        return True

    def delete_task(self, task_id: str) -> bool:
        task = self.tasks.pop(task_id, None)
        if not task:
            return False
        project = self.get_project(task.project_id)
        if project:
            project.task_ids = [tid for tid in project.task_ids if tid != task_id]
        self._save()
        return True


class Storage(DataStorage):
    pass
