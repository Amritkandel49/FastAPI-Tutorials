import pickle
import pandas as pd
from typing import Dict

'''
In real world application, we should use versioning for the model so that we can keep track of different versions of the model and can roll back to previous version if needed

Here we are using a simple versioning scheme

In real world application, we should store the model version in a separate file or database and load it from there.
'''
MODEL_VERSION = '1.0.0'

try:
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")
    
class_labels = model.classes_.tolist()


def model_prediction(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }