variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "agent-sandbox"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "sandbox"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ssh_public_key" {
  description = "Optional SSH public key for debug access"
  type        = string
  default     = ""
}

variable "ami_id" {
  description = "Optional AMI ID to override the default Ubuntu AMI"
  type        = string
  default     = null
}
