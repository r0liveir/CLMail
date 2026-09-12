from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Task, TaskStatus, Coordinator

class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)
    
    def save(self, task: Task) -> None:
        self.session.add(task)

    def get_coordinator_by_id(self, coordinator_id: int) -> Coordinator | None:
        return self.session.get(Coordinator, coordinator_id)
