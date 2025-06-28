#!/bin/bash

# Free Tier EC2 Deployment Script for Titanic API using Terraform

set -e

echo "Deploying Titanic API to EC2 using Terraform (Free Tier Configuration)..."

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "Terraform is not installed. Please install Terraform first."
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Using AWS Account ID: $AWS_ACCOUNT_ID"

# Build and push Docker image to ECR
echo "Building and pushing Docker image to ECR..."

# Get ECR repository URL from Terraform output (if it exists)
if [ -f "terraform.tfstate" ]; then
    ECR_REPO_URL=$(terraform output -raw ecr_repository_url 2>/dev/null || echo "")
fi

if [ -z "$ECR_REPO_URL" ]; then
    # If no state file or output, use the expected format
    ECR_REPO_URL="$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api"
fi

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO_URL

# Build and tag image
docker build -t titanic-api:latest ..
docker tag titanic-api:latest $ECR_REPO_URL:latest

# Push to ECR
docker push $ECR_REPO_URL:latest

echo "Docker image pushed successfully"

# Initialize Terraform (if not already done)
if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init
fi

# Plan Terraform deployment
echo "Planning Terraform deployment..."
terraform plan -out=tfplan

# Apply Terraform deployment
echo "Applying Terraform deployment..."
terraform apply tfplan

# Get the instance details
INSTANCE_IP=$(terraform output -raw instance_public_ip)
echo ""
echo "🎉 Free Tier Deployment completed successfully!"
echo ""
echo "📊 Resource Usage (Free Tier Limits):"
echo "   • EC2 Instance: t2.micro (750 hours/month free)"
echo "   • EBS Storage: 8GB gp2 (30GB free)"
echo "   • ECR: 500MB storage, 500MB data transfer free"
echo "   • CloudWatch: 5GB storage, 5GB ingestion free"
echo ""
echo "🌐 API Access:"
echo "   • API URL: http://$INSTANCE_IP:8000"
echo "   • Health Check: http://$INSTANCE_IP:8000/health"
echo "   • API Documentation: http://$INSTANCE_IP:8000/docs"
echo ""
echo "⚠️  Important Free Tier Notes:"
echo "   • This uses 1 t2.micro instance (free for 12 months)"
echo "   • No load balancer (saves ~$20/month)"
echo "   • Single instance deployment (no auto-scaling)"
echo "   • Monitor usage in AWS Billing Dashboard"
echo ""

# Clean up plan file
rm -f tfplan # Enhanced deployment script
