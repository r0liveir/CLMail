from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .models import Base, Coordinator, Task, TaskStatus

engine = create_engine("sqlite://")

def initialize_db():
    Base.metadata.create_all(engine)

    with Session(engine) as session:
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


def print_tables(session: Session):

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
