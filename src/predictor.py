import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
import os

class TitanicPredictor:
    """Service class for making Titanic survival predictions"""
    
    def __init__(self):
        self.model = None
        self.label_encoders = None
        self.scaler = None
        self.feature_names = None
        self.is_loaded = False
        
    def load_model(self, model_path: str = "models/titanic_model.pkl"):
        """Load the trained model and preprocessors"""
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            self.model = joblib.load(model_path)
            self.label_encoders = joblib.load("models/label_encoders.pkl")
            self.scaler = joblib.load("models/scaler.pkl")
            self.feature_names = joblib.load("models/feature_names.pkl")
            self.is_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.is_loaded = False
            return False
    
    def preprocess_passenger_data(self, passenger_data: Dict[str, Any]) -> np.ndarray:
        """Preprocess passenger data for prediction"""
        try:
            # Convert to DataFrame with proper column names
            df_data = {
                'Pclass': passenger_data.get('pclass'),
                'Sex': passenger_data.get('sex'),
                'Age': passenger_data.get('age'),
                'SibSp': passenger_data.get('sibsp'),
                'Parch': passenger_data.get('parch'),
                'Fare': passenger_data.get('fare'),
                'Embarked': passenger_data.get('embarked'),
                'Name': passenger_data.get('name'),
                'Cabin': passenger_data.get('cabin')
            }
            
            print(f"Input data: {df_data}")
            
            df = pd.DataFrame([df_data])
            
            # Extract title from Name
            if df['Name'].iloc[0]:
                title_match = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False).iloc[0]
                print(f"Extracted title: {title_match}")
                
                # Handle NaN values
                if pd.isna(title_match):
                    df['Title'] = 'Mr'
                else:
                    title = str(title_match)
                    # Map uncommon titles to common ones
                    if title in ['Capt', 'Col', 'Major', 'Dr', 'Rev']:
                        df['Title'] = 'Mr'
                    elif title in ['Mlle', 'Ms']:
                        df['Title'] = 'Miss'
                    elif title == 'Mme':
                        df['Title'] = 'Mrs'
                    else:
                        df['Title'] = title
            else:
                df['Title'] = 'Mr'
            
            # Create family size feature
            df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
            df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
            
            # Extract deck from Cabin
            if df['Cabin'].iloc[0]:
                df['Deck'] = df['Cabin'].str[0]
            else:
                df['Deck'] = 'Unknown'
            
            # Select features for model
            features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 
                        'Title', 'FamilySize', 'IsAlone', 'Deck']
            
            X = df[features].copy()
            print(f"Features before encoding: {X.to_dict('records')[0]}")
            
            # Encode categorical variables
            categorical_features = ['Sex', 'Embarked', 'Title', 'Deck']
            
            for feature in categorical_features:
                if feature in self.label_encoders:
                    try:
                        unique_values = self.label_encoders[feature].classes_
                        value = X[feature].iloc[0]
                        print(f"Encoding {feature}: {value} (available: {unique_values})")
                        
                        if value not in unique_values:
                            # Use the most common value as fallback
                            X[feature] = unique_values[0]
                            print(f"  -> Using fallback: {unique_values[0]}")
                        else:
                            X[feature] = self.label_encoders[feature].transform([value])[0]
                            print(f"  -> Encoded as: {X[feature].iloc[0]}")
                    except Exception as e:
                        print(f"Error encoding {feature}: {e}")
                        # Use the first available value as fallback
                        X[feature] = 0
            
            print(f"Features after encoding: {X.to_dict('records')[0]}")
            
            # Scale numerical features
            numerical_features = ['Age', 'Fare', 'FamilySize']
            X[numerical_features] = self.scaler.transform(X[numerical_features])
            
            print(f"Final features: {X.values[0]}")
            return X.values
            
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            raise
    
    def predict_survival(self, passenger_data: Dict[str, Any]) -> Tuple[bool, float, str]:
        """Predict survival probability and return result with confidence"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        X = self.preprocess_passenger_data(passenger_data)
        
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        survival_prob = probability[1] if len(probability) > 1 else probability[0]
        
        # Determine confidence level
        if survival_prob > 0.8 or survival_prob < 0.2:
            confidence = "High"
        elif survival_prob > 0.6 or survival_prob < 0.4:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        return bool(prediction), float(survival_prob), confidence
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded:
            return {"status": "Model not loaded"}
        
        return {
            "status": "Model loaded",
            "model_type": type(self.model).__name__,
            "feature_count": len(self.feature_names),
            "features": self.feature_names
        } # Added prediction functionality - Mon Jun 30 21:53:40 CEST 2025
# Enhanced input validation - Mon Jun 30 21:53:41 CEST 2025
