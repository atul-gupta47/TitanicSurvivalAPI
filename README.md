# 🚢 Titanic Survival Prediction API

A REST API for predicting survival on the Titanic using machine learning. This project uses the famous Titanic dataset to train a Random Forest model and exposes it through a FastAPI-based REST service.

## 🎯 Features

- **Machine Learning Model**: Random Forest classifier trained on Titanic dataset
- **REST API**: FastAPI-based API with automatic documentation
- **Docker Support**: Containerized application for easy deployment
- **AWS Ready**: Complete infrastructure setup for AWS deployment
- **Health Checks**: Built-in health monitoring
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling and logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│  ML Predictor   │───▶│  Trained Model  │
│   (REST API)    │    │   (Service)     │    │   (joblib)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Docker        │    │   Preprocessors │    │   Titanic       │
│   Container     │    │   (Encoders)    │    │   Dataset       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Docker (for containerization)
- AWS CLI (for deployment)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TitanicSurvivalAPI
```

### 2. Setup and Train Model

```bash
# Run the setup script
python scripts/train_and_deploy.py
```

This script will:
- Install dependencies
- Download the Titanic dataset
- Train the machine learning model
- Test the API
- Build Docker image
- Create deployment scripts

### 3. Test Locally

```bash
# Using Docker Compose
docker-compose up

# Or run directly
cd src
python main.py
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root Endpoint**: http://localhost:8000/

## 📚 API Endpoints

### GET /
Returns API information and available endpoints.

### GET /health
Health check endpoint to verify service status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

### POST /predict
Predict survival probability for a passenger.

**Request Body:**
```json
{
  "pclass": 1,
  "sex": "male",
  "age": 30.0,
  "sibsp": 0,
  "parch": 0,
  "fare": 7.925,
  "embarked": "S",
  "cabin": "C85",
  "name": "Mr. John Doe"
}
```

**Response:**
```json
{
  "survived": false,
  "survival_probability": 0.234,
  "confidence": "Medium"
}
```

### GET /model-info
Get information about the loaded model.

## 🐳 Docker

### Build Image

```bash
docker build -t titanic-api .
```

### Run Container

```bash
docker run -p 8000:8000 titanic-api
```

### Using Docker Compose

```bash
docker-compose up -d
```

## ☁️ AWS Deployment

### Option 1: Using CloudFormation (Recommended)

1. **Deploy Infrastructure**:
```bash
aws cloudformation create-stack \
  --stack-name titanic-api-stack \
  --template-body file://aws-deploy/cloudformation-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=Environment,ParameterValue=production
```

2. **Build and Push Docker Image**:
```bash
# Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t titanic-api .
docker tag titanic-api:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api:latest

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/titanic-api:latest
```

3. **Update ECS Service**:
```bash
aws ecs update-service --cluster production-titanic-cluster --service production-titanic-service --force-new-deployment
```

### Option 2: Using Deployment Script

```bash
# Set your AWS account ID
export AWS_ACCOUNT_ID=your-account-id

# Run deployment
./deploy-aws.sh
```

## 📊 Model Performance

The Random Forest model achieves approximately **82-85% accuracy** on the Titanic dataset with the following features:

- **Passenger Class** (1st, 2nd, 3rd)
- **Sex** (Male/Female)
- **Age**
- **Number of Siblings/Spouses**
- **Number of Parents/Children**
- **Fare**
- **Port of Embarkation**
- **Title** (extracted from name)
- **Family Size** (derived feature)
- **Is Alone** (derived feature)
- **Deck** (extracted from cabin)

## 🔧 Development

### Project Structure

```
TitanicSurvivalAPI/
├── src/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── predictor.py         # ML prediction service
│   └── train_model.py       # Model training script
├── data/
│   └── titanic.csv          # Titanic dataset
├── models/                  # Trained model files
├── aws-deploy/              # AWS deployment files
├── scripts/                 # Utility scripts
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose config
└── README.md               # This file
```

### Adding New Features

1. **New ML Model**: Modify `src/train_model.py`
2. **New API Endpoints**: Add to `src/main.py`
3. **New Data Models**: Update `src/models.py`
4. **New Preprocessing**: Update `src/predictor.py`

### Testing

```bash
# Test the API
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "pclass": 1,
    "sex": "female",
    "age": 25.0,
    "sibsp": 1,
    "parch": 0,
    "fare": 50.0,
    "embarked": "S"
  }'
```

## 🛠️ Troubleshooting

### Common Issues

1. **Model not loading**: Ensure the model is trained first using `python scripts/train_and_deploy.py`

2. **Docker build fails**: Check if all dependencies are in `requirements.txt`

3. **AWS deployment fails**: Verify AWS credentials and permissions

4. **API not responding**: Check if the service is running and healthy

### Logs

- **Local**: Check console output
- **Docker**: `docker logs <container-id>`
- **AWS**: CloudWatch logs in `/ecs/production-titanic-api`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section
---

**Happy Predicting! 🚢✨**

<!-- Enhanced project documentation -->

<!-- Added ECS deployment instructions -->

<!-- Improved documentation -->
