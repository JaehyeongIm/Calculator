from sqlmodel import Field, SQLModel
from typing import Optional

class Expression(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    expr: str
