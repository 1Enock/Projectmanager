from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from .models import ProjectTracker

console = Console()


def get_data_path() -> Path:
    return Path.cwd() / ".projectmanager_data.json"


def get_tracker() -> ProjectTracker:
    return ProjectTracker(get_data_path())


@click.group()
def main() -> None:
    """Project Manager CLI"""


@main.group()
def user() -> None:
    """Manage users"""


@user.command("add")
@click.option("--name", prompt=True, help="Name of the user")
@click.option("--email", prompt=True, help="Email address of the user")
def add(name: str, email: str) -> None:
    tracker = get_tracker()
    user = tracker.create_user(name=name, email=email)
    console.print(f"[green]Created user:[/green] {user.user_id} {user.name} <{user.email}>")


@user.command("list")
def list_users() -> None:
    tracker = get_tracker()
    users = tracker.list_users()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Email")
    for user in users:
        table.add_row(user.user_id, user.name, user.email)
    console.print(table)


@user.command("delete")
@click.argument("user_id")
def delete(user_id: str) -> None:
    tracker = get_tracker()
    success = tracker.delete_user(user_id)
    if success:
        console.print(f"[green]Deleted user {user_id}.[/green]")
    else:
        console.print(f"[red]User {user_id} not found.[/red]")


@main.group()
def project() -> None:
    """Manage projects"""


@project.command("add")
@click.option("--name", prompt=True, help="Project name")
@click.option("--description", prompt=True, help="Project description")
@click.option("--owner", multiple=True, help="User ID to assign as project owner")
def add(name: str, description: str, owner: tuple[str, ...]) -> None:
    tracker = get_tracker()
    project = tracker.create_project(name=name, description=description, owner_user_ids=list(owner))
    console.print(f"[green]Created project:[/green] {project.project_id} {project.name}")


@project.command("list")
def list_projects() -> None:
    tracker = get_tracker()
    projects = tracker.list_projects()
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Owners")
    table.add_column("Tasks")
    for project in projects:
        owners = ", ".join(project.owner_user_ids) or "None"
        table.add_row(project.project_id, project.name, owners, str(len(project.task_ids)))
    console.print(table)


@project.command("assign")
@click.argument("project_id")
@click.argument("user_id")
def assign(project_id: str, user_id: str) -> None:
    tracker = get_tracker()
    project = tracker.assign_project_to_user(project_id, user_id)
    if project:
        console.print(f"[green]Assigned user {user_id} to project {project_id}.[/green]")
    else:
        console.print(f"[red]Project {project_id} not found.[/red]")


@project.command("search")
@click.argument("user_id")
def search(user_id: str) -> None:
    tracker = get_tracker()
    projects = tracker.search_projects_by_user(user_id)
    if not projects:
        console.print(f"[yellow]No projects assigned to {user_id}.[/yellow]")
        return
    table = Table(title=f"Projects for {user_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Tasks")
    for project in projects:
        table.add_row(project.project_id, project.name, str(len(project.task_ids)))
    console.print(table)


@project.command("delete")
@click.argument("project_id")
def delete(project_id: str) -> None:
    tracker = get_tracker()
    success = tracker.delete_project(project_id)
    if success:
        console.print(f"[green]Deleted project {project_id}.[/green]")
    else:
        console.print(f"[red]Project {project_id} not found.[/red]")


@main.group()
def task() -> None:
    """Manage tasks"""


@task.command("add")
@click.option("--project", "project_id", prompt=True, help="Project ID")
@click.option("--title", prompt=True, help="Task title")
@click.option("--description", prompt=True, help="Task description")
@click.option("--assigned-user", default=None, help="User ID assigned to the task")
@click.option("--due-date", default=None, help="Due date for the task (YYYY-MM-DD)")
def add(project_id: str, title: str, description: str, assigned_user: Optional[str], due_date: Optional[str]) -> None:
    tracker = get_tracker()
    task = tracker.create_task(
        title=title,
        description=description,
        project_id=project_id,
        assigned_user_id=assigned_user,
        due_date=due_date,
    )
    console.print(f"[green]Created task:[/green] {task.task_id} {task.title}")


@task.command("list")
@click.option("--project", "project_id", default=None, help="Project ID to filter tasks")
def list_tasks(project_id: Optional[str]) -> None:
    tracker = get_tracker()
    tasks = tracker.list_tasks(project_id=project_id)
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Project")
    table.add_column("Assigned")
    table.add_column("Due")
    table.add_column("Status")
    for task in tasks:
        assigned = task.assigned_user_id or "None"
        due = task.due_date or "None"
        table.add_row(task.task_id, task.title, task.project_id, assigned, due, task.status)
    console.print(table)


@task.command("complete")
@click.argument("task_id")
def complete(task_id: str) -> None:
    tracker = get_tracker()
    task = tracker.update_task_status(task_id, "completed")
    if task:
        console.print(f"[green]Task {task_id} marked completed.[/green]")
    else:
        console.print(f"[red]Task {task_id} not found.[/red]")


@task.command("assign")
@click.argument("task_id")
@click.argument("user_id")
def assign(task_id: str, user_id: str) -> None:
    tracker = get_tracker()
    task = tracker.assign_task(task_id, user_id)
    if task:
        console.print(f"[green]Assigned user {user_id} to task {task_id}.[/green]")
    else:
        console.print(f"[red]Task {task_id} not found.[/red]")


@task.command("delete")
@click.argument("task_id")
def delete(task_id: str) -> None:
    tracker = get_tracker()
    success = tracker.delete_task(task_id)
    if success:
        console.print(f"[green]Deleted task {task_id}.[/green]")
    else:
        console.print(f"[red]Task {task_id} not found.[/red]")
