from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, select, Session
from database import engine, get_session
from sqlalchemy.exc import OperationalError
from model import Student

app = FastAPI()

@app.on_event("startup")
def on_startup():
  try:
    SQLModel.metadata.create_all(engine)
    print("Database Connected Successfully!")
  except OperationalError as e:
    print("Database Connection Failed:")

@app.post("/student")
def add_student(student: Student, session: Session = Depends(get_session) ):
  session.add(student)
  session.commit()
  session.refresh(student)
  return student

@app.get("/students")
def get_student(session: Session = Depends(get_session) ):
  return session.exec(select(Student)).all()

@app.put("/student/{student_id}")
def update_student(student_id: int, updated: Student,session: Session = Depends(get_session)):
  return session.exec(select(Student)).all() 