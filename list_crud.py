from fastapi import FastAPI, Query,Path, HTTPException

app = FastAPI()

list = [1,2,3,4,5,6,7,8,9,10,11,12]


# Get - Fetch Data From Server
@app.get("/Home")
def welcome():
  return {"Message": "Welcome to the page"}

# Get the Array
@app.get("/arrayOfNumbers")
def get_array():
  return list

# Post - Send/Create Data To Server
@app.post("/createArray")
def create_array(list_elements):
  list = list_elements
  return list

# Put - Update Data 
@app.put("/add_element/{value}")
def add_element(index: int = Query(None, description="Add element at an index"), value: int = Path(..., description="add element at the end")):
  if index is None:
    list.append(value)
  else:
    if index < len(list):
      list.insert(index,value)
    else:
      raise HTTPException(status_code=400, detail="Index out of range")
  return list

# Delete - Delete Data
@app.delete("/delete")
def delete_data(index: int = Query(None,description="Delete by index"), value: int = Query(None,description="Delete by Value")):
  if index is None:
    if value in list:
      list.remove(value)
    else:
      raise HTTPException(status_code=400, detail="Element Not in List")
  else:
    if index <= len(list):
      list.pop(index)
    else:
      raise HTTPException(status_code=400, detail="Index out of range")

  return list