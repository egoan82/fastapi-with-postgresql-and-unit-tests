from typing import Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid4, index=True)
    name: str
    first_last_name: str
    second_last_name: Optional[str] = None
    email: str

    __tablename__ = 'users'
