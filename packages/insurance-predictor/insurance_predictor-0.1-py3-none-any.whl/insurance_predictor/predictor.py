from xgboost import XGBClassifier
import pandas as pd
import os
import pkg_resources

class InsurancePredictor:
    def __init__(self):
        # Automatically find the model path
        model_path = pkg_resources.resource_filename('insurance_predictor', 'data/model.json')
        
        # Load the pre-trained model
        self.model = XGBClassifier()
        self.model.load_model(model_path)

    def predict(self, input_features):
        # Make predictions with the pre-trained model
        return self.model.predict(input_features)