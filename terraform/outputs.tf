output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.titanic_api.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.titanic_api.public_dns
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.titanic_api.repository_url
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.titanic_vpc.id
}

output "subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public_subnet.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.titanic_sg.id
}

output "api_url" {
  description = "URL to access the Titanic API"
  value       = "http://${aws_instance.titanic_api.public_ip}:8000"
}

output "health_check_url" {
  description = "URL for API health check"
  value       = "http://${aws_instance.titanic_api.public_ip}:8000/health"
}

output "api_docs_url" {
  description = "URL for API documentation"
  value       = "http://${aws_instance.titanic_api.public_ip}:8000/docs"
} 