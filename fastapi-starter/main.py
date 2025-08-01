from fastapi import FastAPI
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
