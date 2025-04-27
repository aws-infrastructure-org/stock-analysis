# Stock Analysis - AWS Serverless Application

A serverless application for collecting and analyzing stock data using AWS Lambda, API Gateway, S3, and DynamoDB.

## Architecture

This project implements a serverless architecture with:
- Daily data collection Lambda function for stock data
- REST API endpoint for data access and analysis
- S3 buckets for raw and processed stock data storage
- DynamoDB table for analysis results
- Web interface for stock data visualization

## Prerequisites

- Python 3.12 or higher
- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- uv package manager (recommended)

## Project Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd stock-analysis
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies using uv:
```bash
pip install uv
uv pip install -r requirements.txt
```

## Project Structure

```
├── src/                    # Source code directory
│   └── stock_analysis/    # Main package directory
│       ├── api/           # API endpoint handlers
│       ├── collectors/    # Data collection modules
│       ├── models/        # Data models and schemas
│       ├── utils/         # Utility functions
│       ├── static/        # Static assets
│       └── templates/     # HTML templates
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── template.yaml         # SAM template
├── requirements.txt      # Python dependencies
└── setup.py             # Package configuration
```

## Local Development

1. Start the local API:
```bash
sam local start-api
```

2. Test the data collection function locally:
```bash
sam local invoke DataCollectionFunction
```

## Deployment

1. Build the SAM application:
```bash
./build.sh
```

2. Deploy to AWS:
```bash
sam deploy --guided
```

During the guided deployment, you'll need to:
- Choose a stack name
- Select an AWS Region
- Confirm IAM role creation
- Review and confirm other configuration options

### Post-Deployment

After successful deployment, the following resources will be created:
- Two S3 buckets (raw and processed stock data)
- Two Lambda functions (data collection and API)
- API Gateway endpoint
- DynamoDB table for analysis results
- Lambda Layer for dependencies

## Monitoring and Maintenance

- CloudWatch Logs are automatically configured for Lambda functions
- S3 buckets have a 30-day retention policy for raw data
- DynamoDB is configured with on-demand capacity

## Clean Up

To remove all deployed resources:
```bash
sam delete
```

## Environment Variables

Create a `.env` file in the root directory to store environment variables. Use the following template:

```
BUCKET_NAME=test-bucket
TABLE_NAME=test-table
API_KEY=test-api-key
API_ENDPOINT=https://test-api.example.com
```

Ensure that sensitive information like API keys is not hardcoded in the source code.

## GitHub Actions

This project includes a GitHub Actions workflow for CI/CD. The workflow:
- Runs linting and tests on every push or pull request to the `main` branch.
- Deploys the application to AWS if all tests pass.

To use the workflow:
1. Add your AWS credentials as secrets in the GitHub repository (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).
2. Push changes to the `main` branch or create a pull request.

## License

MIT License - See LICENSE file for details