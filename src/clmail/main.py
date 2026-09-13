import os
import sys
from pathlib import Path
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import engine, initialize_db, print_tables
from .repository import TaskRepository
from .service import TaskService

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

## Ponto importante:
# Do jeito que tá, status vai quebrar a validação
# Isso ocorre por que o responses.parse força um modo estrito de structured output
# no servidor. Ele tenta compilar esse schema pra algo rígido e concreto, que o modelo
# tentará inferir e garantir diretamente nos tokens.
# Isso tem algumas vantagens: menos tokens, menos retries, etc
# E especificamente, passar TaskStatus | None quebra as regras de schema do JSON
# Talvez falar sobre como o modelo vai converter isso conceitualmente seja interessante?


# Veremos mais pra frente que isso funciona com PydanticAI, mas também introduz outras complicações
# (retries, etc)
class TaskAction(BaseModel):
    operation: Literal[
        "add_task", "change_status", "change_coordinator", "register_hours", "no_action"
    ]
    task_id: int | None = None
    title: str | None = None
    coordinator_id: int | None = None
    status: Literal["planned", "in_progress", "in_review", "done"] | None = None
    hours: float | None = None


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: clmail <path/to/email.txt>")

    email = Path(sys.argv[1]).read_text(encoding="utf-8")
    print("[Email to be sent]:\n", email)

    # Send email for the LLM, and it returns a valid structured output
    # using Pydantic schema
    # https://developers.openai.com/api/docs/guides/structured-outputs
    response = client.responses.parse(
        model="openai/gpt-oss-120b",
        instructions=system_prompt,
        input=email,
        text_format=TaskAction,
    )

    # Fetch the TaskAction object
    action = response.output_parsed
    if action is None:
        raise SystemExit("Model failed to adhere to schema")

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
            case "add_task":
                result = service.add_task(action.title, action.coordinator_id)
            case "change_status":
                result = service.change_status(action.task_id, action.status)
            case "change_coordinator":
                result = service.change_coordinator(
                    action.task_id, action.coordinator_id
                )
            case "register_hours":
                result = service.register_hours(action.task_id, action.hours)
            case "no_action":
                result = True

        # simple call to make sure agent has picked it up
        print("\n[Action result]:", result)
        print("\n[Database after action]")
        print_tables(session)
