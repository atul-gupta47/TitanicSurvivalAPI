import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import requests

def download_titanic_data():
    """Download Titanic dataset if not already present"""
    data_path = "data/titanic.csv"
    
    if not os.path.exists(data_path):
        print("Downloading Titanic dataset...")
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        response = requests.get(url)
        
        os.makedirs("data", exist_ok=True)
        with open(data_path, 'w') as f:
            f.write(response.text)
        print("Dataset downloaded")
    
    return data_path

def preprocess_data(df):
    """Preprocess the Titanic dataset"""
    df_processed = df.copy()
    
    # Handle missing values
    df_processed['Age'].fillna(df_processed['Age'].median(), inplace=True)
    df_processed['Cabin'].fillna('Unknown', inplace=True)
    df_processed['Embarked'].fillna(df_processed['Embarked'].mode()[0], inplace=True)
    
    # Feature engineering
    df_processed['Title'] = df_processed['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    df_processed['FamilySize'] = df_processed['SibSp'] + df_processed['Parch'] + 1
    df_processed['IsAlone'] = (df_processed['FamilySize'] == 1).astype(int)
    df_processed['Deck'] = df_processed['Cabin'].str[0]
    df_processed['Deck'].fillna('Unknown', inplace=True)
    
    # Select features for model
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 
                'Title', 'FamilySize', 'IsAlone', 'Deck']
    
    X = df_processed[features].copy()
    y = df_processed['Survived']
    
    # Encode categorical variables
    label_encoders = {}
    categorical_features = ['Sex', 'Embarked', 'Title', 'Deck']
    
    for feature in categorical_features:
        le = LabelEncoder()
        X[feature] = le.fit_transform(X[feature].astype(str))
        label_encoders[feature] = le
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_features = ['Age', 'Fare', 'FamilySize']
    X[numerical_features] = scaler.fit_transform(X[numerical_features])
    
    return X, y, label_encoders, scaler

def train_model():
    """Train the Titanic survival prediction model"""
    print("Training model...")
    
    data_path = download_titanic_data()
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records")
    
    X, y, label_encoders, scaler = preprocess_data(df)
    print(f"Preprocessed data with {X.shape[1]} features")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save model and preprocessors
    os.makedirs("models", exist_ok=True)
    
    joblib.dump(model, "models/titanic_model.pkl")
    joblib.dump(label_encoders, "models/label_encoders.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    
    feature_names = X.columns.tolist()
    joblib.dump(feature_names, "models/feature_names.pkl")
    
    print("Model saved")
    return model, label_encoders, scaler, feature_names

if __name__ == "__main__":
    train_model() # Enhanced data preprocessing - Mon Jun 30 21:53:40 CEST 2025
# Improved feature engineering - Mon Jun 30 21:53:40 CEST 2025
