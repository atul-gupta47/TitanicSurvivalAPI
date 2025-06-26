.PHONY: help install train test run docker-build docker-run docker-compose clean deploy-aws

help: ## Show this help message
	@echo "Titanic Survival API - Available Commands"
	@echo "========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-20s %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

train: ## Train the machine learning model
	python scripts/train_and_deploy.py

test: ## Test the API functionality
	python test_api.py

run: ## Run the API locally
	cd src && python main.py

docker-build: ## Build Docker image
	docker build -t titanic-api .

docker-run: ## Run Docker container
	docker run -p 8000:8000 titanic-api

docker-compose: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker Compose
	docker-compose down

clean: ## Clean up generated files
	rm -rf models/*.pkl
	rm -rf __pycache__
	rm -rf src/__pycache__
	find . -name "*.pyc" -delete

deploy-aws: ## Deploy to AWS (requires AWS CLI setup)
	@echo "Deploying to AWS..."
	@echo "Please ensure you have:"
	@echo "1. AWS CLI configured"
	@echo "2. AWS_ACCOUNT_ID environment variable set"
	@echo "3. Appropriate AWS permissions"
	./deploy-aws.sh

setup: install train ## Complete setup (install + train)
	@echo "Setup completed!"

dev: setup run ## Development setup and run
	@echo "Development server started at http://localhost:8000"

all: setup docker-build docker-compose ## Complete setup with Docker
	@echo "Complete setup with Docker completed!"
	@echo "API available at http://localhost:8000"
	@echo "Documentation at http://localhost:8000/docs" # Enhanced build automation
