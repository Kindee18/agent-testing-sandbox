#!/bin/bash
set -e

echo "Starting Agent Workflow Tests..."

# Install dependencies
pip install pytest pyyaml

# Run tests
pytest agent-tests/test_fragile_sites.py --junitxml=test-results.xml

echo "Tests completed successfully."
