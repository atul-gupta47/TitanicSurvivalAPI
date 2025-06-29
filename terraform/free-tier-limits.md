# AWS Free Tier Limits & Our Usage

This document explains how our Titanic API deployment stays within AWS Free Tier limits.

## 🆓 AWS Free Tier Overview

AWS Free Tier provides **12 months** of free access to many AWS services with specific usage limits.

## 📊 Service-by-Service Breakdown

### 1. **EC2 (Elastic Compute Cloud)**

| Free Tier Limit | Our Usage | Status |
|----------------|-----------|--------|
| **750 hours/month** of t2.micro or t3.micro | 1 t2.micro instance | ✅ Within limit |
| **Linux, RHEL, or SLES** | Amazon Linux 2 | ✅ Eligible |
| **1 year** from account creation | New account | ✅ Eligible |

**Our Configuration:**
- Instance Type: `t2.micro` (1 vCPU, 1 GB RAM)
- OS: Amazon Linux 2
- Usage: 24/7 = 744 hours/month (within 750 limit)

### 2. **EBS (Elastic Block Store)**

| Free Tier Limit | Our Usage | Status |
|----------------|-----------|--------|
| **30 GB** of gp2 storage | 8 GB volume | ✅ Within limit |
| **1 million I/O requests** | Minimal usage | ✅ Within limit |
| **1 GB of snapshot storage** | Not used | ✅ Within limit |

**Our Configuration:**
- Volume Size: 8 GB
- Volume Type: gp2
- Delete on Termination: true

### 3. **ECR (Elastic Container Registry)**

| Free Tier Limit | Our Usage | Status |
|----------------|-----------|--------|
| **500 MB** storage | ~100 MB (Docker image) | ✅ Within limit |
| **500 MB** data transfer | Minimal pull/push | ✅ Within limit |

**Our Usage:**
- Docker Image Size: ~100 MB
- Data Transfer: < 100 MB/month
- Storage: < 200 MB (including layers)

### 4. **CloudWatch**

| Free Tier Limit | Our Usage | Status |
|----------------|-----------|--------|
| **5 GB** data ingestion | Minimal logs | ✅ Within limit |
| **5 GB** data storage | 1 day retention | ✅ Within limit |
| **10 custom metrics** | Basic metrics only | ✅ Within limit |

**Our Configuration:**
- Log Retention: 1 day (minimizes storage)
- Metrics: Basic EC2 metrics only

### 5. **VPC & Networking**

| Service | Free Tier | Our Usage | Status |
|---------|-----------|-----------|--------|
| **VPC** | Always free | 1 VPC | ✅ Free |
| **Security Groups** | Always free | 1 security group | ✅ Free |
| **Internet Gateway** | Always free | 1 IGW | ✅ Free |
| **Route Tables** | Always free | 1 route table | ✅ Free |
| **Subnets** | Always free | 1 subnet | ✅ Free |

### 6. **IAM (Identity and Access Management)**

| Service | Free Tier | Our Usage | Status |
|---------|-----------|-----------|--------|
| **IAM Users** | Always free | 1 user | ✅ Free |
| **IAM Roles** | Always free | 1 role | ✅ Free |
| **IAM Policies** | Always free | 2 policies | ✅ Free |

## 🚫 What We Excluded (Cost Reasons)

### 1. **Application Load Balancer (ALB)**
- **Cost**: ~$20/month
- **Free Tier**: 15 GB data processing
- **Decision**: Excluded to stay free
- **Impact**: Direct access to EC2 instance

### 2. **Auto Scaling Group**
- **Cost**: Additional instances beyond free tier
- **Free Tier**: Only 1 instance free
- **Decision**: Single instance deployment
- **Impact**: No high availability

### 3. **HTTPS/SSL Certificates**
- **Cost**: Requires load balancer
- **Free Tier**: ACM certificates free with ALB
- **Decision**: HTTP only
- **Impact**: No encryption (development use)

### 4. **Multiple Availability Zones**
- **Cost**: Additional instances
- **Free Tier**: Only 1 instance free
- **Decision**: Single AZ deployment
- **Impact**: No disaster recovery

## 💰 Cost Breakdown

| Service | Free Tier Limit | Monthly Cost if Exceeded |
|---------|----------------|-------------------------|
| **EC2 t2.micro** | 750 hours | $8.47/month |
| **EBS 8GB** | 30GB | $0.80/month |
| **ECR** | 500MB storage | $0.10/month |
| **CloudWatch** | 5GB storage | $0.50/month |
| **Data Transfer** | 1GB out | $0.09/month |
| **Total Potential Cost** | - | **$9.96/month** |

## ⚠️ Important Warnings

### 1. **12-Month Limit**
- Free tier expires after 12 months
- Monitor AWS Billing Dashboard
- Set up billing alerts

### 2. **Usage Monitoring**
```bash
# Check current usage
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### 3. **Billing Alerts**
- Set up CloudWatch billing alarms
- Monitor usage in AWS Console
- Check free tier usage dashboard

## 🔄 Upgrade Path

When free tier expires or you need more features:

### Phase 1: Basic Production (~$30/month)
```hcl
instance_type = "t3.small"      # $15/month
desired_capacity = 2            # High availability
# Add load balancer: $20/month
```

### Phase 2: Full Production (~$100/month)
```hcl
instance_type = "t3.medium"     # $30/month
desired_capacity = 3            # Auto scaling
# Load balancer + HTTPS: $25/month
# Additional monitoring: $20/month
```

## 📋 Monitoring Checklist

- [ ] Check AWS Billing Dashboard weekly
- [ ] Monitor EC2 instance usage
- [ ] Review CloudWatch logs size
- [ ] Check ECR storage usage
- [ ] Set up billing alerts
- [ ] Review free tier usage dashboard

## 🛡️ Cost Protection

### 1. **Budget Alerts**
```bash
# Create budget alert
aws budgets create-budget \
  --account-id YOUR_ACCOUNT_ID \
  --budget '{"BudgetName":"Free Tier Budget","BudgetLimit":{"Amount":"5","Unit":"USD"},"TimeUnit":"MONTHLY"}' \
  --notifications-with-subscribers '[{"Notification":{"ComparisonOperator":"GREATER_THAN","NotificationType":"ACTUAL","Threshold":80,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"Address":"your-email@example.com","SubscriptionType":"EMAIL"}]}]'
```

### 2. **Resource Tagging**
```hcl
tags = {
  Environment = "free-tier"
  Project     = "titanic-api"
  CostCenter  = "development"
}
```

### 3. **Regular Cleanup**
```bash
# Clean up unused resources
terraform destroy  # When not needed
``` 
<!-- Enhanced free tier documentation -->
