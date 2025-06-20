terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
resource "aws_vpc" "titanic_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.environment}-titanic-vpc"
  }
}

resource "aws_internet_gateway" "titanic_igw" {
  vpc_id = aws_vpc.titanic_vpc.id

  tags = {
    Name = "${var.environment}-titanic-igw"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.titanic_vpc.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.environment}-titanic-public-subnet"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.titanic_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.titanic_igw.id
  }

  tags = {
    Name = "${var.environment}-titanic-public-rt"
  }
}

resource "aws_route_table_association" "public_rta" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group
resource "aws_security_group" "titanic_sg" {
  name        = "${var.environment}-titanic-sg"
  description = "Security group for Titanic API"
  vpc_id      = aws_vpc.titanic_vpc.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "API Port"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.environment}-titanic-sg"
  }
}

# ECR Repository (Free Tier: 500MB storage, 500MB data transfer)
resource "aws_ecr_repository" "titanic_api" {
  name                 = "titanic-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# IAM Role for EC2
resource "aws_iam_role" "ec2_role" {
  name = "${var.environment}-titanic-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "ecr_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.environment}-titanic-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# User data script
data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    ecr_repository_url = aws_ecr_repository.titanic_api.repository_url
    aws_region         = var.aws_region
  }
}

# Free Tier: Single EC2 Instance (no Auto Scaling Group)
resource "aws_instance" "titanic_api" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.titanic_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  user_data              = base64encode(data.template_file.user_data.rendered)

  tags = {
    Name = "${var.environment}-titanic-api"
  }

  # Free Tier: Use gp2 EBS volume (30GB free)
  root_block_device {
    volume_size = 8
    volume_type = "gp2"
    delete_on_termination = true
  }
}

# CloudWatch Log Group (Free Tier: 5GB storage, 5GB data ingestion)
resource "aws_cloudwatch_log_group" "titanic_logs" {
  name              = "/ec2/${var.environment}-titanic-api"
  retention_in_days = 1  # Free Tier: Keep logs for 1 day to minimize storage
} 