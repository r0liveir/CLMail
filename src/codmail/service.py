from codmail.models import Task, TaskStatus
from codmail.repository import TaskRepository

class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def add_task(
        self,
        title: str | None = None,
        coordinator_id: int | None = None,
    ) -> bool:
        if coordinator_id is None or title is None:
            return False

        if self.repo.get_coordinator_by_id(coordinator_id) is None:
            return False

        task = Task(title=title, coordinator_id=coordinator_id)
        self.repo.save(task)
        self.repo.session.commit()

        return True 
    
    def change_status(
        self, 
        task_id: int,
        status: TaskStatus,
    ) -> bool:
        task = self.repo.get_by_id(task_id)
        if task is None:
            return False
        
        task.status = status
        self.repo.session.commit()
        return True
    
    def change_coordinator(
        self,
        task_id: int,
        coordinator_id: int,
    ) -> bool:
        task = self.repo.get_by_id(task_id)
        coordinator = self.repo.get_coordinator_by_id(coordinator_id)
        if task is None or coordinator is None:
            return False

        task.coordinator_id = coordinator_id
        self.repo.session.commit()
        return True

    def register_hours(
        self,
        task_id: int | None,
        hours: float | None,
    ) -> bool:
        if task_id is None or hours is None or hours <= 0:
            return False

        task = self.repo.get_by_id(task_id)
        if task is None:
            return False

        task.hours += hours
        self.repo.session.commit()
        return True
