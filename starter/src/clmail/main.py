import sys
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from .database import engine, initialize_db, print_tables
from .repository import TaskRepository
from .service import TaskService

####
# AULA: definir aqui TaskAction, system_prompt, model e agent.
####

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: clmail <caminho/para/email.txt>")

    email = Path(sys.argv[1]).read_text(encoding="utf-8")

    ####
    # AULA: chamar o modelo e obter response.output.
    ####


    initialize_db()
    with Session(engine) as session:
        service = TaskService(TaskRepository(session))

        print("\n[Banco antes da ação]")
        print_tables(session)
            
        #####
        # AULA: rotear action.operation com match/case.
        #####

        #print("\n[Ação aplicada]", result)
        print("\n[Banco depois da ação]")
        print_tables(session)
