from pydantic import BaseModel

class Patient(BaseModel):
    name:str
    age:int


patient_info = {
    "name": "John Doe",
    "age": 30
}

patient1 = Patient(**patient_info)



def get_patient_info(patient1 : Patient):
    return {
        "name": patient1.name,
        "age": patient1.age
    }

print(get_patient_info(patient1))

patient2 = Patient(name="New John", age = '30') # pydantic will convert '30' to int
print(get_patient_info(patient2))  

