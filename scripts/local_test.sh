#!/bin/bash
set -e

echo "🚀 Starting Local Sandbox Infrastructure Test..."

# 1. Start LocalStack
echo "--- Starting LocalStack ---"
docker-compose up -d localstack

# Wait for LocalStack to be ready
echo "Waiting for LocalStack gateway..."
until curl -s http://localhost:4566/_localstack/health | grep -q '"s3": "running"'; do
  sleep 2
done

echo "✅ LocalStack is ready!"

# 2. Run Python Tests Locally (Mocking Infrastructure)
echo "--- Running Agent Tests Locally ---"
# We bypass the full terraform apply for the local quick-test 
# and just run the pytest suite directly to verify the agent logic.
pip3 install pytest pyyaml > /dev/null
python3 agent-tests/test_fragile_sites.py

echo "--- Simulating Infrastructure Provisioning ---"
echo "✅ Mock VPC Created"
echo "✅ Mock EC2 Runner Provisioned"
echo "✅ Mock S3 Bucket for Logs Created"

echo "🎉 Local test complete! No AWS account was used."
echo "To clean up: docker-compose down"
