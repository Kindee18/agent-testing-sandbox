#!/bin/bash
# setup_secrets.sh - Automate GitHub Secrets configuration for the Infra-Testing project

set -e

echo "🚀 Starting Portfolio Project Secrets Setup..."

# 1. Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed."
    echo "Please install it from https://cli.github.com/ and run 'gh auth login' before continuing."
    exit 1
fi

# 2. Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Error: You are not logged into GitHub CLI."
    echo "Please run 'gh auth login' to authenticate."
    exit 1
fi

# 3. Collect AWS Credentials
echo ""
echo "--- AWS Credentials ---"
read -p "Enter your AWS_ACCESS_KEY_ID: " aws_id
read -sp "Enter your AWS_SECRET_ACCESS_KEY: " aws_secret
echo ""

# 4. Generate SSH Key Pair
echo ""
echo "--- SSH Key Generation ---"
KEY_PATH="./infra_deploy_key"
if [ -f "$KEY_PATH" ]; then
    echo "⚠️  SSH key already exists at $KEY_PATH. Skipping generation."
else
    echo "Generating new SSH key pair at $KEY_PATH..."
    ssh-keygen -t rsa -b 4096 -f "$KEY_PATH" -N "" -q
    echo "✅ SSH keys generated."
fi

# 5. Push Secrets to GitHub
echo ""
echo "--- Uploading Secrets to GitHub ---"

echo "Pushing AWS_ACCESS_KEY_ID..."
echo "$aws_id" | gh secret set AWS_ACCESS_KEY_ID

echo "Pushing AWS_SECRET_ACCESS_KEY..."
echo "$aws_secret" | gh secret set AWS_SECRET_ACCESS_KEY

echo "Pushing SSH_PRIVATE_KEY..."
gh secret set SSH_PRIVATE_KEY < "$KEY_PATH"

echo "Pushing TF_VAR_ssh_public_key..."
# We use the public key content for the Terraform variable
pub_key=$(cat "${KEY_PATH}.pub")
echo "$pub_key" | gh secret set TF_VAR_SSH_PUBLIC_KEY

echo ""
echo "🎉 SUCCESS! Your GitHub repository is now configured for Real AWS Mode."
echo "--- Important: Security Notice ---"
echo "A private key was generated at: $KEY_PATH"
echo "NEVER commit this file to your repository."
echo "The .gitignore will protect you, but keep it safe elsewhere or delete it after verification."
