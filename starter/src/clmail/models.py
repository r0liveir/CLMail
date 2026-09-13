import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TaskStatus(enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class Base(DeclarativeBase):
    pass


class Coordinator(Base):
    __tablename__ = "coordinators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    tasks: Mapped[list["Task"]] = relationship(back_populates="coordinator")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    coordinator_id: Mapped[int] = mapped_column(ForeignKey("coordinators.id"))
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PLANNED)
    hours: Mapped[float] = mapped_column(default=0.0)

    coordinator: Mapped["Coordinator"] = relationship(back_populates="tasks")
