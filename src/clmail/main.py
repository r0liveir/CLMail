from typing import Literal
from .service import TaskService
from .repository import TaskRepository
from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.groq import GroqModel
import sys
from pathlib import Path
from .database import engine, print_tables, initialize_db
from sqlalchemy.orm import Session
from .models import TaskStatus

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

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: clmail <path/to/email.txt>")

    email = Path(sys.argv[1]).read_text(encoding="utf-8")
    print("[Email to be sent]:\n", email)
    
    # send to the LLM to parse
    response = agent.run_sync(email, model_settings=ModelSettings(max_tokens=500))
    action = response.output

    print("[Received response]:\n", action)
    
    with Session(engine) as session:
        # initial seed
        initialize_db()

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
