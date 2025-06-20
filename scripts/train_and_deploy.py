#!/usr/bin/env python3
"""
Script to train the Titanic model and prepare for deployment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"{description}...")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    return True

def main():
    """Main function to train model and prepare deployment"""
    print("Titanic Survival API - Setup")
    print("=" * 40)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("Failed to install dependencies")
        return False
    
    # Train the model
    print("Training model...")
    try:
        # Add the project root (parent of scripts/) to sys.path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        from src.train_model import train_model
        train_model()
        print("Model training completed")
    except Exception as e:
        print(f"Model training failed: {str(e)}")
        return False
    
    # Test the API
    print("Testing API...")
    if not run_command("python -c \"import sys; sys.path.insert(0, '.'); from src.main import app; print('API imports successfully')\"", "Testing API imports"):
        print("API test failed")
        return False
    
    # Create directories
    print("Creating directories...")
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Verify model files
    model_files = [
        "models/titanic_model.pkl",
        "models/label_encoders.pkl", 
        "models/scaler.pkl",
        "models/feature_names.pkl"
    ]
    
    for model_file in model_files:
        if not os.path.exists(model_file):
            print(f"Model file missing: {model_file}")
            return False
    
    print("All model files verified")
    
    # Test Docker build
    print("Building Docker image...")
    if not run_command("docker build -t titanic-api .", "Building Docker image"):
        print("Docker build failed")
        return False
    
    print("Docker build successful")
    
    # Create deployment script
    print("Creating deployment script...")
    
    aws_deploy_script = """#!/bin/bash
# AWS ECS Deployment Script for Titanic API

echo "Deploying Titanic API to AWS ECS..."

# Build and push Docker image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag titanic-api:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api:latest

# Update ECS service
aws ecs update-service --cluster titanic-cluster --service titanic-service --force-new-deployment

echo "Deployment completed"
"""
    
    with open("deploy-aws.sh", "w") as f:
        f.write(aws_deploy_script)
    
    os.chmod("deploy-aws.sh", 0o755)
    
    print("Deployment setup completed")
    
    # Final instructions
    print("\n" + "=" * 40)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Test locally: docker-compose up")
    print("2. Visit: http://localhost:8000/docs")
    print("3. Deploy to AWS: ./deploy-aws.sh")
    print("=" * 40)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 