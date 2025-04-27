#!/bin/bash

# Exit on error
set -e

# Create layer directory structure
echo "Creating Lambda layer directory structure..."
mkdir -p layer/python

echo "Installing dependencies into the layer..."
python3 -m pip install --platform manylinux2014_x86_64 --implementation cp --python-version 3.9 --only-binary=:all: --upgrade -r requirements.txt --target layer/python
python3 -m pip install --platform manylinux2014_x86_64 --implementation cp --python-version 3.9 --only-binary=:all: --upgrade yfinance pandas --target layer/python

echo "Installing the stock_analysis package..."
python3 -m pip install -e . --target layer/python

# Build SAM application
sam build --config-file samconfig.toml

echo "Done! You can now deploy using: sam deploy"