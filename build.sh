#!/bin/bash

# Exit on error
set -e

# Create a temporary directory for building the Lambda layer
TEMP_DIR=$(mktemp -d)
LAYER_DIR="$TEMP_DIR/python"

echo "Creating Lambda layer directory structure..."
mkdir -p "$LAYER_DIR"

echo "Installing dependencies into the layer..."
pip install -r requirements.txt --target "$LAYER_DIR"

echo "Installing the stock_analysis package..."
pip install -e . --target "$LAYER_DIR"

# Check if S3_BUCKET is set
if [ -z "$S3_BUCKET" ]; then
  echo "Error: S3_BUCKET environment variable is not set. Please set it to your S3 bucket name."
  exit 1
fi

# Build SAM application with S3 bucket using samconfig.toml
export S3_BUCKET=aws-sam-cli-managed-default-samclisourcebucket-vfojv2l9rdow
sam build --config-file samconfig.toml

echo "Done! You can now deploy using: sam deploy"