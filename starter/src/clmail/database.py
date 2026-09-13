from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .models import Base, Coordinator, Task, TaskStatus


engine = create_engine("sqlite://")


def initialize_db() -> None:
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        alex = Coordinator(id=1, name="Fulano da Silva")
        bia = Coordinator(id=2, name="Beatriz Camargo")
        task = Task(
            id=101,
            title="Preparar roadmap do próximo trimestre",
            status=TaskStatus.PLANNED,
            coordinator=alex,
        )
        session.add_all([alex, bia, task])
        session.commit()


def print_tables(session: Session) -> None:
    print("Responsáveis:")
    for coordinator in session.scalars(select(Coordinator)):
        print(f"  id={coordinator.id}, nome={coordinator.name!r}")

    print("Tarefas:")
    for task in session.scalars(select(Task)):
        print(
            f"  id={task.id}, título={task.title!r}, "
            f"responsável={task.coordinator_id}, "
            f"status={task.status.value!r}, horas={task.hours}"
        )
