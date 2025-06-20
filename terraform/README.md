# Titanic API - Free Tier EC2 Deployment with Terraform

This directory contains Terraform configuration for deploying the Titanic Survival API to AWS EC2 instances using **Free Tier eligible resources only**.

## 🆓 Free Tier Architecture

- **EC2 Instance**: Single t2.micro instance (750 hours/month free)
- **EBS Storage**: 8GB gp2 volume (30GB free)
- **ECR Repository**: 500MB storage, 500MB data transfer free
- **CloudWatch**: 5GB storage, 5GB data ingestion free
- **VPC**: Free (no additional cost)
- **Security Groups**: Free

## 🚫 What's NOT Included (to stay free)

- ❌ **Load Balancer** (~$20/month)
- ❌ **Auto Scaling Group** (additional instances cost money)
- ❌ **HTTPS/SSL** (requires load balancer)
- ❌ **Multiple instances** (scaling costs money)

## Prerequisites

1. **Terraform** (>= 1.0)
2. **AWS CLI** configured with appropriate permissions
3. **Docker** for building and pushing images
4. **AWS Free Tier account** (first 12 months)

## Quick Start

1. **Navigate to the terraform directory**:
   ```bash
   cd terraform
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Deploy using the script**:
   ```bash
   chmod +x deploy-ec2.sh
   ./deploy-ec2.sh
   ```

## Manual Deployment

1. **Build and push Docker image**:
   ```bash
   # From project root
   docker build -t titanic-api:latest .
   
   # Get ECR repository URL
   ECR_REPO_URL=$(terraform output -raw ecr_repository_url)
   
   # Login and push
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO_URL
   docker tag titanic-api:latest $ECR_REPO_URL:latest
   docker push $ECR_REPO_URL:latest
   ```

2. **Deploy infrastructure**:
   ```bash
   terraform plan
   terraform apply
   ```

## Configuration

### Free Tier Variables

```hcl
aws_region = "us-east-1"
environment = "free-tier"
instance_type = "t2.micro"      # Free tier eligible
desired_capacity = 1            # Single instance
min_size = 1                    # No scaling
max_size = 1                    # No scaling
use_free_tier = true           # Enable free tier optimizations
```

### Instance Types (Free Tier)

- **t2.micro**: 1 vCPU, 1 GB RAM (750 hours/month free)
- **t3.micro**: 2 vCPU, 1 GB RAM (750 hours/month free)

## Accessing the API

After deployment, the API will be available at:
- **API URL**: `http://<instance-public-ip>:8000`
- **Health Check**: `http://<instance-public-ip>:8000/health`
- **API Documentation**: `http://<instance-public-ip>:8000/docs`

## 📊 Free Tier Usage Monitoring

### AWS Free Tier Limits

| Service | Free Tier Limit | Our Usage |
|---------|----------------|-----------|
| **EC2** | 750 hours/month | 1 t2.micro instance |
| **EBS** | 30GB gp2 | 8GB volume |
| **ECR** | 500MB storage | ~100MB (Docker image) |
| **CloudWatch** | 5GB storage | Minimal logs |

### Cost Breakdown

- **EC2 t2.micro**: $0/month (free tier)
- **EBS 8GB**: $0/month (free tier)
- **ECR**: $0/month (free tier)
- **CloudWatch**: $0/month (free tier)
- **Data Transfer**: $0/month (minimal usage)
- **Total**: **$0/month** 🎉

## Monitoring

- **CloudWatch Logs**: `/ec2/free-tier-titanic-api`
- **EC2 Metrics**: CPU, memory, network usage
- **AWS Billing Dashboard**: Monitor free tier usage

## Security

- **Security Group**: Allows HTTP (80), API (8000), SSH (22)
- **IAM Role**: EC2 instances have minimal required permissions
- **VPC**: Isolated network with public subnet

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

## ⚠️ Important Free Tier Notes

1. **12-Month Limit**: Free tier expires after 12 months
2. **Usage Monitoring**: Check AWS Billing Dashboard regularly
3. **No Load Balancer**: Direct access to EC2 instance
4. **Single Instance**: No high availability
5. **Manual Scaling**: No auto-scaling capabilities

## Troubleshooting

### Common Issues

1. **ECR Login Failed**: Ensure AWS credentials are configured
2. **Instance Health Checks Failing**: Check if Docker containers are running
3. **API Not Accessible**: Verify security group rules

### SSH Access

To SSH into the instance (if needed):
```bash
# Get instance ID
aws ec2 describe-instances --filters "Name=tag:Name,Values=free-tier-titanic-api" --query 'Reservations[].Instances[].InstanceId' --output text

# SSH (requires key pair)
ssh -i your-key.pem ec2-user@<instance-public-ip>
```

### Logs

View application logs on EC2:
```bash
# SSH into instance
ssh ec2-user@<instance-ip>

# Check Docker logs
docker-compose logs titanic-api

# Check system logs
sudo journalctl -u docker
```

## 🚀 Upgrading from Free Tier

When you're ready to upgrade (after 12 months or for production):

1. **Add Load Balancer**: Modify `main.tf` to include ALB
2. **Enable Auto Scaling**: Change to Auto Scaling Group
3. **Add HTTPS**: Configure SSL certificates
4. **Increase Resources**: Use larger instance types

Example upgrade:
```hcl
instance_type = "t3.small"      # $15/month
desired_capacity = 2            # High availability
# Add load balancer configuration
``` 