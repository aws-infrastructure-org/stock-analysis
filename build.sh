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

echo "Building SAM application..."
sam build

echo "Done! You can now deploy using: sam deploy"