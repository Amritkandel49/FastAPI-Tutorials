from pydantic import BaseModel

class Address(BaseModel):
    street: str
    country: str
    city: str
    state: str
    pincode: str

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    address: Address

patient_info = {
    "name": "John Doe",
    "age": 30,
    "weight": 70.5,
    "address": {
        "street": "123 Main St",
        "country": "USA",
        "city": "New York",
        "state": "NY",
        "pincode": "10001"
    }
}    


patient1 = Patient(**patient_info)
def get_patient_info(patient: Patient):
    print(f'''
        "name": {patient.name},
        "age": {patient.age},
        "weight": {patient.weight},
        "address": {{
            "street": {patient.address.street},
            "country": {patient.address.country},
            "city": {patient.address.city},
            "state": {patient.address.state},
            "pincode": {patient.address.pincode}
        }}
    ''')


get_patient_info(patient1)