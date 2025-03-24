# predict_model.py
# This file contains functions to load  and make predictions for streamlit app.

##############################################
# Importing necessary libraries
##############################################

import joblib


##############################################
# Functions
##############################################
def load_model(model_path):
    """
    Load a trained model from the specified file path.

    Args:
        model_path: Path to the model file.

    Returns:
        The loaded model.
    """
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None
    
def predict(model, data):
    """
    Use the given model to make predictions on the provided data.

    Args:
        model: The trained model to use for predictions.
        data: The input data for which predictions are to be made.

    Returns:
        The predictions made by the model.
    """
    try:
        predictions = model.predict(data)
        return predictions
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None