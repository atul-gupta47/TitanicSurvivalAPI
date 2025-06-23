#!/usr/bin/env python3
"""
Test script for the Titanic Survival API
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"Health check passed: {data}")
            return data.get('model_loaded', False)
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check error: {str(e)}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"Root endpoint: {data}")
            return True
        else:
            print(f"Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Root endpoint error: {str(e)}")
        return False

def test_model_info():
    """Test the model info endpoint"""
    print("Testing model info...")
    
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"Model info: {data}")
            return True
        else:
            print(f"Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Model info error: {str(e)}")
        return False

def test_prediction(passenger_data):
    """Test the prediction endpoint"""
    print(f"Testing prediction for: {passenger_data.get('name', 'Unknown')}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=passenger_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Prediction successful:")
            print(f"  Survived: {data['survived']}")
            print(f"  Probability: {data['survival_probability']:.3f}")
            print(f"  Confidence: {data['confidence']}")
            return True
        else:
            print(f"Prediction failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("Titanic Survival API - Test Suite")
    print("=" * 40)
    
    # Wait for API to be ready
    print("Waiting for API to be ready...")
    time.sleep(5)
    
    # Test endpoints
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Model Info", test_model_info),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed_tests += 1
        else:
            print(f"{test_name} failed")
    
    # Test predictions with different scenarios
    test_passengers = [
        {
            "name": "Mr. John Smith",
            "pclass": 3,
            "sex": "male",
            "age": 22.0,
            "sibsp": 1,
            "parch": 0,
            "fare": 7.925,
            "embarked": "S",
            "cabin": None
        },
        {
            "name": "Mrs. Jane Doe",
            "pclass": 1,
            "sex": "female",
            "age": 29.0,
            "sibsp": 0,
            "parch": 0,
            "fare": 211.3375,
            "embarked": "S",
            "cabin": "B42"
        },
        {
            "name": "Master. Tommy Wilson",
            "pclass": 2,
            "sex": "male",
            "age": 8.0,
            "sibsp": 3,
            "parch": 1,
            "fare": 69.55,
            "embarked": "S",
            "cabin": "C22"
        }
    ]
    
    print(f"Testing predictions with {len(test_passengers)} scenarios...")
    
    for passenger in test_passengers:
        if test_prediction(passenger):
            passed_tests += 1
        total_tests += 1
    
    # Summary
    print("\n" + "=" * 40)
    print(f"Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("All tests passed! API is working correctly.")
        return True
    else:
        print("Some tests failed. Please check the API.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) # Enhanced test coverage - Mon Jun 30 21:53:40 CEST 2025
