from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.model import MODEL_VERSION, model, model_prediction
from schema.prediction_response import PredictionResponse
from typing import Dict

app = FastAPI()        
        
@app.get('/')
def home():
    return JSONResponse(status_code = 200, content = {'message': 'Welcome to Insurance Premium Prediction API.'})


# health check route
'''
We should have a health check endpoint to verify that the API is running and responsive.
'/' url are generally human readable home pages, human can confirm that API is running by looking at this url
but '/health' url is generally used by monitoring tools to check the health of the API.
Different bots from platforms like AWS, AZURE, GCP etc can use this url to check the health of the API.
'''
@app.get('/health')
def health_check():
    return JSONResponse(status_code=200, content={
        'status': 'API is healthy and running.',
        'model_version': MODEL_VERSION,
        'model_loaded': True if model else False
        })

# post route for the model
@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:

        prediction = model_prediction(user_input)

        return JSONResponse(status_code=200, content={'response': prediction})
    
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))