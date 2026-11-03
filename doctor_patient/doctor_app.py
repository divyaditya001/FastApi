from fastapi import FastAPI, Path, HTTPException,Query
from pydantic import BaseModel
import json

app = FastAPI()

class Patient(BaseModel):
  name: str
  city: str
  age: int
  gender: str
  height: int
  weight: int
  bmi: int
  verdict: str


# loading data from JSON file
def load_data():
  with open('patients.json', 'r') as f:
    data = json.load(f)
  return data

# saving data to json file
def save_data(data):
  with open('patients.json', 'w') as f:
    json.dump(data,f,indent=4)

# Welcone Page
@app.get("/")
def hello():
  return {"Message": "Welcome"}

# View Patients Data
@app.get("/all_patients")
def view_patient_data():
  data = load_data()  
  return data

# Get a Particular Patient Details From It's ID
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(...,description = 'ID of the patient in DB', example='P001')):
  data = load_data()
  if patient_id in data:
    return data[patient_id]
  else:
    raise HTTPException(status_code=404, detail = 'Patient not found')

# Get sorted patient data
@app.get("/sort")
def sort_patient(sort_by: str = Query(...,description="Sort on the basis of height, weight, bmi or age"), order: str = Query('asc', description="Sort in Ascending or Descending", example="desc")):

  valid_fields = ['height', 'weight', 'bmi', 'age']
  if sort_by not in valid_fields:
    raise HTTPException(status_code=400, detail=f"Invalid Fields, Select from {valid_fields}")

  if order not in ['asc','desc']:
    raise HTTPException(status_code=400, detail=f"Invalid Fields, Select from 'asc','desc'")

  dictionary = load_data()
  sort_order = True if order == 'desc' else False
  sortes_data = sorted(dictionary.values(), key = lambda items: items[sort_by], reverse=sort_order)

  return sortes_data

# Add a new patient
@app.post("/addpatient")
def add_patient(patient: Patient):
  data = load_data()
  # Findind the next patient ID
  last_id = max(data.keys())
  next_num = int(last_id[1:]) + 1
  next_id = f"P{next_num:03d}"

  # updating the dict and json file
  data[next_id] = patient.model_dump()
  save_data(data)

  return {"Message": f"New Patient Details: {data}"}


# Delete patient 
@app.put("/delete/{patient_id}")
def delete_patient(patient_id: str = Path(..., description="Enter Patient ID to be deleted", example="P002")): 
  data = load_data()
  data.pop(patient_id)
  # save data
  save_data(data)

  return {"Message": f"New Patient Details: {data}"}

# Update patient detail
@app.put("/update/{patient_id}")
def update_patient(patient_id: str = Path(...,description="Patient ID"), field: str = Query(None,description="Field to be updated"), value = Query(None,description="Value to be Updated")):
  data = load_data()
  fields = ["name","city","age","gender","height","weight","bmi","verdict"]

  if field not in fields:
    raise HTTPException(status_code=400,detail="Invalid Field")
  else:
    data[patient_id][field] = value
  # save data
  save_data(data)

  return {"Message": f"New Patient Details: {data}"}
  
  