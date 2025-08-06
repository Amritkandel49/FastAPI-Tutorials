from pydantic import BaseModel, EmailStr, Field, computed_field 
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    allergies: List[str]
    married: bool
    contact_details: Dict[str, str]

    @computed_field(return_type=float)
    @property
    def bmi(self):
        return self.weight / (self.height **2)


patient_info = {
    "name": "John Doe",
    "email": "abs@tu.edu.np",
    "age": 80, 
    "weight": 70.5, # in kgs
    "height": 1.75,  # height in meters
    "allergies": ["dust", "pollens"],
    "married": False,
    "contact_details": {
        "emergency_contact": "9876543210",
        "phone": "123-456-7890"
    }
}


patient = Patient(**patient_info)
def get_patient_info(patient: Patient):
    print(f'''
        "name": {patient.name},
        "email": {patient.email},
        "age": {patient.age},
        "weight": {patient.weight},
        "height": {patient.height},
        "bmi": {patient.bmi},
        "allergies": {patient.allergies},
        "married": {patient.married},
        "contact_details": {patient.contact_details}
    ''')

get_patient_info(patient)