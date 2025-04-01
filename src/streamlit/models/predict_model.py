# predict_model.py
# This file contains functions to load  and make predictions for streamlit app.

##############################################
# Importing necessary libraries
##############################################

import joblib
import pandas as pd
from . import prepare
import os
import xgboost as xgb

##############################################
# Functions
##############################################

def load_model(model_path):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, model_path)

        if not os.path.exists(full_path):
            print("❌ Fichier introuvable : ", full_path)
            return None

        model = joblib.load(full_path)
        return model

    except Exception as e:
        print(f"⚠️ Une erreur est survenue lors du chargement du modèle : {e}")
        return None

#################################################
# Loading the binary classification model
#################################################

binary = load_model("xgboost_model_binary.pkl")
multiclass = load_model("xgboost_model_multiclass.pkl")


def predict_binary(df, model=binary):
    """
    Use the given binary classification model to make predictions on the provided data.

    Args:
        model: The trained binary classification model to use for predictions.
        data: The input data for which predictions are to be made.

    Returns:
        The binary predictions made by the model.
    """
    try:
        data = prepare.prepare(df)
        predictions = model.predict(data)
        print(predictions)
        return predictions
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None
    
def predict_multiclass(data, model=multiclass):
    """
    This function is specifically designed for multiclass classification.

    Args:
        model: The trained binary classification model to use for predictions.
        data: The input data for which predictions are to be made.

    Returns:
        The binary predictions made by the model.
    """
    try:
        data = prepare.prepare_multiclass(data)
        predictions = model.predict(data)
        return predictions
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None

################################################

