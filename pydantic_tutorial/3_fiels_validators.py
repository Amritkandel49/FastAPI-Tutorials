from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Optional, Annotated, Dict


# Pydantic also provides various built-in complex data types line EmailStr to validate email addresses 

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    allergies: List[str]
    married: bool
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        # abc.gmail.com
        domain_name = value.split('@')[-1]
        if domain_name not in ['tu.edu.np', 'ioe.edu.np']:
            raise ValueError('Email domain must be tu.edu.np or ioe.edu.np')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    

    # practicing for after mode in field validation
    @field_validator('age', mode='after')
    @classmethod
    def validate_Age(cls, value):
        if value > 100 or value < 0:
            raise ValueError('Age must be between 0 and 100')
        return value
    
    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, model):
        if 'emergency_contact' not in model.contact_details and model.age>60:
            raise ValueError('Emergency contact is required for patients above 60 years of age')
        return model

patient_info = {
    "name": "John Doe",
    "email": "abs@tu.edu.np",
    "age": 80, 
    "weight": 70.5,
    "allergies": ["dust", "pollens"],
    "married": False,
    "contact_details": {
        "emergency_contact": "9876543210",
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