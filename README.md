# Automated Sandbox Infrastructure Testing for AI Agent Workflows

## Project Overview
This project demonstrates a production-grade DevOps workflow for testing AI agent extraction logic in an ephemeral AWS sandbox. It solves the problem of "fragile" website updates breaking agent workflows by validating changes in a temporary environment before deployment.

## Key Features
- **Ephemeral Infrastructure**: Created and destroyed on every pipeline run using Terraform.
- **Agent Validation**: Automated Python tests simulate agent workflows against target domains.
- **CI/CD Integration**: Fully automated via GitHub Actions.
- **Secure by Design**: Restricted security groups and IAM roles with least-privilege access.
- **Cost Efficient**: Designed to run within the AWS Free Tier (t3.micro).

## Tech Stack
- **Cloud**: AWS (VPC, EC2, S3, IAM)
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Testing**: Python, Pytest
- **Containerization**: Docker

## Repository Structure
```text
agent-testing-sandbox/
│
├── terraform/                # Infrastructure as Code
│   ├── modules/vpc/          # Networking module
│   ├── main.tf               # Orchestration logic
│   ├── variables.tf          # Configurable parameters
│   └── outputs.tf            # Key IP/Resource outputs
│
├── agent-tests/              # AI Agent test scripts
│   ├── test_fragile_sites.py # Mock extraction tests
│   └── test_config.yaml      # Test configuration
│
├── docker/                   # Deployment assets
│   └── Dockerfile            # Containerized runner
│
├── .github/workflows/        # Automation
│   └── pipeline.yml          # End-to-end CI/CD workflow
│
└── scripts/                  # Helper scripts
    └── run_tests.sh          # Test execution logic
```

## How It Works (Deployment Flow)
1. **Developer Push**: A new agent workflow or config update is pushed to the repository.
2. **Provisioning**: GitHub Actions triggers Terraform to create a dedicated VPC and EC2 instance.
3. **Deployment**: The agent code and test scripts are deployed to the EC2 instance.
4. **Execution**: The runner executes `pytest` against the target sites, validating semantic output.
5. **Teardown**: Regardless of success or failure, Terraform destroys all resources to minimize costs.

## Prerequisites
- AWS Account with `AdministratorAccess` (for demo purposes)
- GitHub Repository Secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`

## Local Testing (No AWS Required)
If you do not have a working AWS account or want to verify the logic locally:
1. Ensure you have **Docker** and **Docker Compose** installed.
2. Run the local test script:
   ```bash
   bash scripts/local_test.sh
   ```
4. (Optional) Run a dependency-free **Smoke Test** to verify extraction logic:
   ```bash
   python3 scripts/smoke_test.py
   ```
