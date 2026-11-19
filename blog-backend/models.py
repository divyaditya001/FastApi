from sqlmodel import SQLModel, Field
from typing import Optional

class Blog(SQLModel,table=True):
  id: Optional[int] = Field(default=None,primary_key=True)
  title: str
  description: str
  author: str
  is_published: bool
  words: int

class BlogUpdate(SQLModel):
  title: Optional[str] = None
  description: Optional[str] = None
  author: Optional[str] = None
  is_published: Optional[bool] = None
  words: Optional[int] = None