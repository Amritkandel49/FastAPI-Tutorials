#  building more complex model then in 1.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional


# Pydantic also provides various built-in complex data types line EmailStr to validate email addresses 

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    allergies: Optional[List[str]] = None 
    married: bool = False
    contact_details: dict[str, str]

patient_info = {
    "name": "John Doe",
    "email": "abs@gmail.com",
    "age": 30,
    "weight": 70.5,
    # "allergies": ["dust", "pollens"],
    # "married": True,
    "contact_details": {
        "phone": "123-456-7890"
    }
}

# Optional is used to allow fields to be omitted
patient = Patient(**patient_info)
def get_patient_info(patient: Patient):
    print(f'''
        "name": {patient.name},
        "email": {patient.email},
        "age": {patient.age},
        "weight": {patient.weight},
        "allergies": {patient.allergies},
        "married": {patient.married},
        "contact_details": {patient.contact_details}
    ''')

get_patient_info(patient)