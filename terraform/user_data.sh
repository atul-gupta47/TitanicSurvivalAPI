#!/bin/bash

# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Add ec2-user to docker group
usermod -a -G docker ec2-user

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Create application directory
mkdir -p /opt/titanic-api
cd /opt/titanic-api

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  titanic-api:
    image: ${ecr_repository_url}:latest
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# Login to ECR
aws ecr get-login-password --region ${aws_region} | docker login --username AWS --password-stdin ${ecr_repository_url}

# Pull and start the application
docker-compose pull
docker-compose up -d

# Create a simple health check script
cat > /opt/titanic-api/health_check.sh << 'EOF'
#!/bin/bash
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "API is healthy"
    exit 0
else
    echo "API is unhealthy"
    exit 1
fi
EOF

chmod +x /opt/titanic-api/health_check.sh

# Set up log rotation
cat > /etc/logrotate.d/titanic-api << 'EOF'
/opt/titanic-api/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 ec2-user ec2-user
}
EOF # Enhanced user data script
