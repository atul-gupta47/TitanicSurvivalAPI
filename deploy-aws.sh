#!/bin/bash
# AWS ECS Deployment Script for Titanic API

echo "Deploying Titanic API to AWS ECS..."

# Build and push Docker image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag titanic-api:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api:latest

# Update ECS service
aws ecs update-service --cluster titanic-cluster --service titanic-service --force-new-deployment

echo "Deployment completed"
# Enhanced deployment script
