from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    name: str
    created_at: datetime = Field(default_factory=datetime.now, index=True)


class Task(TaskBase, table=True):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    project_id: UUID = Field(..., foreign_key="project.id")


class TaskCreate(TaskBase):
    ...


class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    project_id: UUID


class TaskUpdate(SQLModel):
    name: str | None = None
    project_id: UUID | None = None
