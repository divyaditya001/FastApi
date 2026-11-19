from fastapi import FastAPI
import random
from typing import Optional
from pydantic import BaseModel
import string
import secrets



app = FastAPI()

@app.on_event("startup")

class Student(BaseModel):
  name: str
  email: str
  course: str
  age: int
  is_enrolled: Optional[bool] = False

def generate_opt():
  return random.randint(1,99999)

def password(len):
  all_digits = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(secrets.choice(all_digits) for _ in range(len))
  return password

@app.get("/")
def home():
  return {"Message": "Hello World!!"}


# Get all students
@app.get("/students")
def get_students():
  return {"Message": "All Students Here.."}

# Create Student
@app.post("/student")
def create_student(student: Student):
  # return {"Message": "Student Created"}
  return student

# Get Student from student_id
@app.get("/student/{student_id}")
def get_student_id(student_id):
  return {"Message": "Single Student Data"}

# Change Student Data
@app.put("/student/{student_id}")
def update_student(student_id, student: Student):
  return {"Message": "Updated Student Data"}

# Delete Student Data
@app.delete("/student/{student_id}")
def update_student(student_id):
  return {"Message": "Deleted Student Data"}

# 
@app.get("/otp")
def get_otp():
  return generate_opt()

# 65-90,97-122,48-57