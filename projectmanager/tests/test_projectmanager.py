from pathlib import Path

import pytest
from click.testing import CliRunner

from projectmanager.cli import main
from projectmanager.models import ProjectTracker


def test_project_tracker_creates_and_retrieves_data(tmp_path: Path) -> None:
    data_path = tmp_path / "data.json"
    tracker = ProjectTracker(data_path)

    user = tracker.create_user(name="Alice", email="alice@example.com")
    assert user.user_id.startswith("u")
    assert tracker.get_user(user.user_id).name == "Alice"

    project = tracker.create_project(name="Launch", description="A launch project", owner_user_ids=[user.user_id])
    assert project.project_id.startswith("p")
    assert tracker.search_projects_by_user(user.user_id)[0].project_id == project.project_id

    task = tracker.create_task(
        title="Run tests",
        description="Ensure CLI works",
        project_id=project.project_id,
        assigned_user_id=user.user_id,
        due_date="2026-12-31",
    )
    assert task.task_id.startswith("t")
    assert tracker.get_task(task.task_id).status == "pending"

    completed = tracker.update_task_status(task.task_id, "completed")
    assert completed is not None
    assert completed.status == "completed"

    tracker.delete_task(task.task_id)
    assert tracker.get_task(task.task_id) is None
    tracker.delete_project(project.project_id)
    assert tracker.get_project(project.project_id) is None


def test_cli_can_add_and_list_user(tmp_path: Path) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=str(tmp_path)):
        result = runner.invoke(main, ["user", "add"], input="Bob\nbob@example.com\n")
        assert result.exit_code == 0
        assert "Created user" in result.output

        result = runner.invoke(main, ["user", "list"])
        assert result.exit_code == 0
        assert "Bob" in result.output


def test_cli_creates_project_and_task(tmp_path: Path) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=str(tmp_path)):
        result = runner.invoke(main, ["user", "add"], input="Casey\ncasey@example.com\n")
        assert result.exit_code == 0
        user_id = result.output.split()[3]

    result = runner.invoke(
        main,
        ["project", "add", "--name", "WebApp", "--description", "Build website", "--owner", user_id],
        env={"PWD": str(tmp_path)},
    )
    assert result.exit_code == 0
    assert "Created project" in result.output

    project_id = result.output.split()[3]
    result = runner.invoke(
        main,
        [
            "task",
            "add",
            "--project",
            project_id,
            "--title",
            "Design UI",
            "--description",
            "Mock screen flows",
            "--assigned-user",
            user_id,
            "--due-date",
            "2026-08-01",
        ],
        env={"PWD": str(tmp_path)},
    )
    assert result.exit_code == 0
    assert "Created task" in result.output
