from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session,Field,select
from database import engine, get_session
from sqlalchemy.exc import OperationalError
from models import Blog, BlogUpdate
from typing import Any

app = FastAPI()

@app.on_event("startup")
def startup():
  try:
    SQLModel.metadata.create_all(engine)
    print("Database Connected Successfully")
  except OperationalError as e:
    print("Database Connection Failed:",e)


@app.get("/")
def home():
  return {"Message": "Welcome home"}

# Create blog
@app.post("/blog")
def create_blog(blog: Blog, session: Session = Depends(get_session)):
   session.add(blog)
   session.commit()
   session.refresh(blog)
   return blog

# Get All blogs
@app.get("/blogs")
def get_blogs(session: Session = Depends(get_session)):
  return session.exec(select(Blog)).all()

# Get blog by blog id
@app.get("/blog/{blog_id}")
def get_blogs(blog_id: int,session: Session = Depends(get_session)):
  blog = session.get(Blog, blog_id)
  # blog = session.exec(select(Blog).where(Blog.id == blog_id)).first()
  if not blog:
    raise HTTPException(status_code=404, detail="Student not found")
  return blog

# Update blog
@app.put("/update/{blog_id}")
def update_blog(blog_id: int, new_data: BlogUpdate = Query(description="Only provide data to be changed and delete the rest") ,session: Session = Depends(get_session)):

  blog = session.get(Blog, blog_id)
  if not blog:
    raise HTTPException(status_code=404, detail="Blog not found")

  new_data_dict = new_data.model_dump(exclude_unset=True)
  blog.sqlmodel_update(new_data_dict)
  
  # valid_fields = [column.name for column in Blog.__table__.columns]
  # if field not in valid_fields:
  #   raise HTTPException(status_code=404, detail="Invalid field")
  # Updating the field with new data
  # setattr(blog,field,new_data)

  session.add(blog)
  session.commit()
  session.refresh(blog)
  return blog


# Delete blog
@app.delete("/detele/{blog_id}")
def delete_blog(blog_id : int, session: Session = Depends(get_session)):
  blog = session.get(Blog, blog_id)

  session.delete(blog)
  session.commit()
  return {"Message": f"Blog Deleted, With Blog ID: {blog_id}"}
  

  