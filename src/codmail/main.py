from typing import Literal
from .models import Base, TaskStatus, Coordinator, Task
from .service import TaskService
from .repository import TaskRepository
from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.groq import GroqModel
import sys
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

model = GroqModel("openai/gpt-oss-120b")

system_prompt = """
You're an assistant for administrative tasks, parsing user sent e-mails into
structured actions.

Allowed operations:
    - add_task
    - change_status
    - change_coordinator
    - register_hours
    - no_action

Never invent IDs, pull them from emails.
Use no_action for incomplete or unrelated e-mails.
"""

class TaskAction(BaseModel):
    operation: Literal["add_task", "change_status", "change_coordinator", "register_hours", "no_action"]
    task_id: int | None = None
    title: str | None = None
    coordinator_id: int | None = None
    status: TaskStatus | None = None
    hours: float | None = None

agent = Agent(
    model=model,
    output_type=TaskAction,
    instructions=system_prompt
)

def seed_db(session: Session) -> None:
    alex = Coordinator(id=1, name="Fulado da Silva")
    sam = Coordinator(id=2, name="Ciclano Camargo")

    task = Task(
        id=101,
        title="Prepare Q3 kickoff roadmap",
        status=TaskStatus.PLANNED,
        coordinator=alex,
    )

    session.add_all([alex, sam, task])
    session.commit()

def print_tables(session: Session) -> None:
    print("Coordinators:")
    for coordinator in session.scalars(select(Coordinator)):
        print(f"  id={coordinator.id}, name={coordinator.name!r}")

    print("Tasks:")
    for task in session.scalars(select(Task)):
        print(
            f"  id={task.id}, title={task.title!r}, "
            f"coordinator_id={task.coordinator_id}, "
            f"status={task.status.value!r}, hours={task.hours}"
        )

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: codmail <path/to/email.txt>")

    email = Path(sys.argv[1]).read_text(encoding="utf-8")
    print("[Email to be sent]:\n", email)
    
    # send to the LLM to parse
    response = agent.run_sync(email, model_settings=ModelSettings(max_tokens=500))
    action = response.output

    print("[Received response]:\n", action)
    
    ## Initialize sqlite session
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # initial seed
        seed_db(session)

        # connect stuff
        repository = TaskRepository(session=session)
        service = TaskService(repo=repository)

        print("\n[Database before action]")
        print_tables(session)

        match action.operation:
            case 'add_task':
                result = service.add_task(action.title, action.coordinator_id)
            case 'change_status':
                result = service.change_status(action.task_id, action.status)
            case 'change_coordinator':
                result = service.change_coordinator(action.task_id, action.coordinator_id)
            case 'register_hours':
                result = service.register_hours(action.task_id, action.hours)
            case 'no_action':
                result = True
            case _:
                raise SystemExit("An unexpected error has occured")
        
        # simple call to make sure agent has picked it up
        print("\n[Action result]:", result)
        print("\n[Database after action]")
        print_tables(session)
