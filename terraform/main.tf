module "vpc" {
  source       = "./modules/vpc"
  project_name = var.project_name
  environment  = var.environment
}

# --- Security Groups ---
resource "aws_security_group" "agent_runner" {
  name        = "${var.project_name}-runner-sg"
  description = "Security group for AI agent runner instance"
  vpc_id      = module.vpc.vpc_id

  # Allow outbound internet access for web scraping
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-runner-sg"
    Environment = var.environment
  }
}

# --- IAM Role for EC2 ---
resource "aws_iam_role" "agent_runner_role" {
  name = "${var.project_name}-runner-role"

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

# IAM Policy for S3 logging
resource "aws_iam_policy" "logging_policy" {
  name        = "${var.project_name}-logging-policy"
  description = "Policy to allow agent runner to upload logs to S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          aws_s3_bucket.logs.arn,
          "${aws_s3_bucket.logs.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "logging_attach" {
  role       = aws_iam_role.agent_runner_role.name
  policy_arn = aws_iam_policy.logging_policy.arn
}

resource "aws_iam_instance_profile" "runner_profile" {
  name = "${var.project_name}-runner-profile"
  role = aws_iam_role.agent_runner_role.name
}

# --- S3 Bucket for Logs ---
resource "aws_s3_bucket" "logs" {
  bucket        = "${var.project_name}-test-logs-${data.aws_caller_identity.current.account_id}"
  force_destroy = true # Good for ephemeral sandbox

  tags = {
    Name        = "${var.project_name}-logs"
    Environment = var.environment
  }
}

data "aws_caller_identity" "current" {}

# --- EC2 Instance ---
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "agent_runner" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = module.vpc.public_subnet_id
  vpc_security_group_ids = [aws_security_group.agent_runner.id]
  iam_instance_profile   = aws_iam_instance_profile.runner_profile.name

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io python3-pip
              systemctl start docker
              systemctl enable docker
              EOF

  tags = {
    Name        = "${var.project_name}-runner"
    Environment = var.environment
  }
}
