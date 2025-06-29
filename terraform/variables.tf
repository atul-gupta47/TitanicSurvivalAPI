variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "free-tier"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type (Free Tier: t2.micro or t3.micro)"
  type        = string
  default     = "t2.micro"
}

variable "desired_capacity" {
  description = "Desired number of instances in Auto Scaling Group (Free Tier: 1 instance)"
  type        = number
  default     = 1
}

variable "min_size" {
  description = "Minimum number of instances in Auto Scaling Group (Free Tier: 1 instance)"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum number of instances in Auto Scaling Group (Free Tier: 1 instance)"
  type        = number
  default     = 1
}

variable "use_free_tier" {
  description = "Enable Free Tier optimizations"
  type        = bool
  default     = true
} # Added Terraform variables
# Free tier optimizations
