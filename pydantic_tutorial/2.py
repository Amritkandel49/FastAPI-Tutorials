#  building more complex model then in 1.py
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Optional, Annotated


# Pydantic also provides various built-in complex data types line EmailStr to validate email addresses 

class Patient(BaseModel):
    # name: str = Field(max_length=50)
    # we can use Annotated to add metadata to field as below
    name: Annotated[str, Field(max_length=50, description="Name of the patient, max length 50 characters", example="John Doe", title="Patient Name")]

    email: EmailStr
    linkedin_url: Optional[AnyUrl] = None # AnyUrl validates the format of the given URL
    age: int
    weight: Annotated[float, Field(gt = 0, description="Weight of the patient in kg, must be greater than 0", strict= True)]
    allergies: Annotated[Optional[List[str]], Field(max_length=5, default=None)] # List of strings with a maximum length of 5
    married: Annotated[bool, Field(default = False, description="Marital status of the patient")]
    contact_details: dict[str, str]

patient_info = {
    "name": "John Doe",
    "email": "abs@gmail.com",
    "linkedin_url": "https://www.linkedin.com/in/johndoe",
    # "linkedin_url": "not a valid url",  # Uncommenting this will raise
    "age": 30,
    "weight": 70.5,
    # "weight": -1, # This will raise a validation error because weight must be greater than 0

    "allergies": ["dust", "pollens"],
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
        "linkedin_url": {patient.linkedin_url},
        "age": {patient.age},
        "weight": {patient.weight},
        "allergies": {patient.allergies},
        "married": {patient.married},
        "contact_details": {patient.contact_details}
    ''')

get_patient_info(patient)