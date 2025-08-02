from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

# loading data from the patient.json file
def load_data():
    with open('patient.json', 'r') as f:
        return json.load(f) 
        # return f


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Starter!"}

@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}


@app.get('/square/{number}')
def square_number(number: int):
    return {"number": number, "square": number ** 2}


@app.get("/view")
def view():
    data = load_data()
    return {"data": data}



@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example = "P001" )):
    data = load_data()
    if patient_id in data:
        return {"Patient" : data[patient_id]} 
    else:
        raise HTTPException(status_code = 404, detail = f"Patient with id {patient_id} not found.")
    

#  query parameters
'''
We will have two option 
1. sort by either [height,  weight, bmi]
2. sort in order [asc, desc]
'''

@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description="Sort by [weight, height, bmi]"), order : str = Query('asc', description="In which order you want to sort the patient details")):
    field_values = ['weight', 'height', 'bmi']
    sort_order = ['asc', 'desc']

    if sort_by not in field_values:
        raise HTTPException(status_code=404, detail= f"Invalid field. Select from {field_values}")
    
    if order not in sort_order:
        raise HTTPException(status_code=404, detail= f"Invalid sort order. Select from {sort_order}")
    
    data = load_data()

    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse= True if order == 'desc' else False)

    return sorted_data