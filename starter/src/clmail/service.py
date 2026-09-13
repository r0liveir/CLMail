from .models import Task, TaskStatus
from .repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def add_task(
        self,
        title: str | None,
        coordinator_id: int | None,
    ) -> bool:
        if title is None or coordinator_id is None:
            return False

        if self.repo.get_coordinator_by_id(coordinator_id) is None:
            return False

        self.repo.save(Task(title=title, coordinator_id=coordinator_id))
        self.repo.session.commit()
        return True

    def change_status(
        self,
        task_id: int | None,
        status: TaskStatus | None,
    ) -> bool:
        """TODO: implement change status"""
        pass
