from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient", example=["P001"])]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    age: Annotated[int, Field(..., lt=100, gt = 0, description="The age of the patient")]
    city: Annotated[str, Field(..., description="The city of the patient")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="The gender of the patient")]
    weight: Annotated[float, Field(..., description="The weight of the patient", gt = 0)]
    height: Annotated[float, Field(..., description="The height of the patient", gt=0)]

    @computed_field(return_type=float)
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    

    @computed_field(return_type=str)
    @property
    def bmi_category(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"
        

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, lt=100, gt = 0)]
    city: Annotated[Optional[str], Field(default=None)]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None, gt = 0)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]

# loading data from the patient.json file
def load_data():
    with open('patient.json', 'r') as f:
        return json.load(f) 
        # return f

# to save the new json data to the file
def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)


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


@app.post('/create/')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    #check if patient id already exists
    if patient.id in data:
        # if exists return error message
        raise HTTPException(status_code=400, detail=f"Patient with id {patient.id} already exists.")
    
    # if not exists add the new patient to the data
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save the updated data back to the json file
    save_data(data)
    
    # return success message with patient details
    return JSONResponse(status_code = 201, content = {'message': 'Patient created successfully', 'patient': data[patient.id]})


@app.put('/edit/{patient_id}')
def edit_patient(patient_id: str, patient_update: PatientUpdate):
    #load existing data
    data = load_data()

    # check if patient id exists
    if patient_id not in data: 
        raise HTTPException(status_code = 404, detail = f"Patient with ID {patient_id} not found.")
    
    #update only the fields that are provided in the request
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_object.model_dump(exclude={'id'})

    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient information updated successfully', 'patient': data[patient_id]})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # load existing data
    data = load_data()

    #check if patient id exists or not
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = f"Patient with id {patient_id} not found.")

    #if exists delete the patient
    deleted_data = data.pop(patient_id)

    save_data(data)

    #return response message
    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully', 'patient': deleted_data})