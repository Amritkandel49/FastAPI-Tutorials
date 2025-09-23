# Patient Management System - Backend

A RESTful API backend built with FastAPI for managing patient data in healthcare applications. This system provides comprehensive CRUD operations for patient records with automatic BMI calculations and health categorization.

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete patient records
- **Automatic BMI Calculation**: Automatically calculates BMI based on height and weight
- **Health Categorization**: Automatically categorizes patients based on BMI (Underweight, Normal, Overweight, Obese)
- **Data Validation**: Robust input validation using Pydantic models
- **Sorting Capabilities**: Sort patients by weight, height, or BMI in ascending/descending order
- **JSON Data Storage**: Simple file-based storage system
- **Interactive API Documentation**: Auto-generated Swagger UI documentation

## Technology Stack

- **Framework**: FastAPI
- **Data Validation**: Pydantic
- **Data Storage**: JSON file
- **Language**: Python 3.10
- **Documentation**: Automatic OpenAPI/Swagger

## Prerequisites

- Python 3.10+
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Amritkandel49/Patient-Management-System-backend.git
   cd Patient-Management-System-backend
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

## Running the Application

1. **Navigate to the project directory**
   ```bash
   cd patient_management_system
   ```

2. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the application**
   - API Server: `http://localhost:8000`
   - Interactive API Documentation: `http://localhost:8000/docs`
   - Alternative API Documentation: `http://localhost:8000/redoc`

## Data Model

### Patient Model
```python
{
    "id": "P001",           # Unique patient identifier
    "name": "John Doe",     # Patient's full name
    "age": 30,              # Age (1-99)
    "city": "New York",     # City of residence
    "gender": "Male",       # Gender (Male/Female/Other)
    "weight": 70.5,         # Weight in kg
    "height": 1.75,         # Height in meters
    "bmi": 23.02,          # Auto-calculated BMI
    "bmi_category": "Normal" # Auto-calculated category
}
```

## API Endpoints

### 1. **Welcome Endpoint**
- **GET** `/`
- **Description**: Welcome message for the API
- **Response**: 
  ```json
  {"message": "Welcome to the FastAPI Starter!"}
  ```

### 2. **Greeting Endpoint**
- **GET** `/greet/{name}`
- **Description**: Personalized greeting
- **Parameters**: 
  - `name` (path): Name to greet
- **Response**: 
  ```json
  {"message": "Hello, John!"}
  ```

### 3. **Square Number**
- **GET** `/square/{number}`
- **Description**: Calculate square of a number
- **Parameters**: 
  - `number` (path): Integer to square
- **Response**: 
  ```json
  {"number": 5, "square": 25}
  ```

### 4. **View All Patients**
- **GET** `/view`
- **Description**: Retrieve all patient records
- **Response**: 
  ```json
  {
    "data": {
      "P001": {...},
      "P002": {...}
    }
  }
  ```

### 5. **Get Single Patient**
- **GET** `/patient/{patient_id}`
- **Description**: Retrieve a specific patient by ID
- **Parameters**: 
  - `patient_id` (path): Patient ID (e.g., "P001")
- **Response**: 
  ```json
  {"Patient": {"name": "John Doe", "age": 30, ...}}
  ```
- **Error**: 404 if patient not found

### 6. **Sort Patients**
- **GET** `/sort`
- **Description**: Sort patients by specified criteria
- **Query Parameters**: 
  - `sort_by` (required): Sort field ("weight", "height", "bmi")
  - `order` (optional): Sort order ("asc", "desc") - defaults to "asc"
- **Example**: `/sort?sort_by=bmi&order=desc`
- **Response**: Array of sorted patient objects

### 7. **Create Patient**
- **POST** `/create/`
- **Description**: Create a new patient record
- **Request Body**: Patient object (JSON)
- **Example**:
  ```json
  {
    "id": "P001",
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "gender": "Male",
    "weight": 70.5,
    "height": 1.75
  }
  ```
- **Response**: 201 Created with patient data
- **Error**: 400 if patient ID already exists

### 8. **Update Patient**
- **PUT** `/edit/{patient_id}`
- **Description**: Update existing patient information
- **Parameters**: 
  - `patient_id` (path): Patient ID to update
- **Request Body**: Partial patient object (only fields to update)
- **Example**:
  ```json
  {
    "age": 31,
    "weight": 72.0
  }
  ```
- **Response**: 200 OK with updated patient data
- **Error**: 404 if patient not found

### 9. **Delete Patient**
- **DELETE** `/delete/{patient_id}`
- **Description**: Delete a patient record
- **Parameters**: 
  - `patient_id` (path): Patient ID to delete
- **Response**: 200 OK with deleted patient data
- **Error**: 404 if patient not found

## Project Structure

```
Patient-Management-System-backend/
├── patient_management_system/
│   ├── main.py              # Main application file
│   ├── patient.json         # Data storage file
│   └── __pycache__/         # Python cache files
├── pydantic_tutorial/       # Learning examples
│   ├── 1.py
│   ├── 2.py
│   ├── 3_fiels_validators.py
│   ├── 4_computed_field.py
│   ├── 5_nested_model.py
│   └── 6_serialization.py
└── README.md               # This file
```

## Key Features Explained

### Automatic BMI Calculation
The system automatically calculates BMI using the formula: `BMI = weight / (height²)`

### Health Categorization
Based on BMI values:
- **Underweight**: BMI < 18.5
- **Normal**: 18.5 ≤ BMI < 24.9
- **Overweight**: 25 ≤ BMI < 29.9
- **Obese**: BMI ≥ 30

### Data Validation
- Age: Must be between 1-99
- Weight & Height: Must be greater than 0
- Gender: Must be "Male", "Female", or "Other"
- ID: Required for patient creation

## Testing the API

You can test the API using:

1. **Swagger UI**: `http://localhost:8000/docs`
2. **curl commands**:
   ```bash
   # Get all patients
   curl -X GET "http://localhost:8000/view"
   
   # Create a patient
   curl -X POST "http://localhost:8000/create/" \
        -H "Content-Type: application/json" \
        -d '{"id":"P001","name":"John Doe","age":30,"city":"NYC","gender":"Male","weight":70,"height":1.75}'
   
   # Get a specific patient
   curl -X GET "http://localhost:8000/patient/P001"
   ```

3. **Python requests**:
   ```python
   import requests
   
   # Create a patient
   response = requests.post("http://localhost:8000/create/", json={
       "id": "P001",
       "name": "John Doe",
       "age": 30,
       "city": "New York",
       "gender": "Male",
       "weight": 70.5,
       "height": 1.75
   })
   ```

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input data or duplicate patient ID
- **404 Not Found**: Patient not found or invalid sort parameters
- **422 Unprocessable Entity**: Data validation errors

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Patient search functionality
- [ ] Medical history tracking
- [ ] Appointment scheduling
- [ ] Data export capabilities
- [ ] Unit tests and CI/CD pipeline

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

⭐ **Don't forget to star this repository if you found it helpful!**