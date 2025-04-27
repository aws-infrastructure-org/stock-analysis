import json
import pytest
import boto3
from decimal import Decimal
from moto import mock_dynamodb
from stock_analysis.api.handler import lambda_handler


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def dynamodb(aws_credentials):
    """Create mock DynamoDB."""
    with mock_dynamodb():
        yield boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture
def dynamodb_table(dynamodb):
    """Create mock DynamoDB table."""
    table = dynamodb.create_table(
        TableName="test-table",
        KeySchema=[
            {"AttributeName": "symbol", "KeyType": "HASH"},
            {"AttributeName": "timestamp", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "symbol", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )

    # Add test data
    table.put_item(
        Item={
            "symbol": "AAPL",
            "timestamp": "2025-04-27T10:00:00Z",
            "price": "150.00",
            "data": {
                "quoteResponse": {
                    "result": [
                        {
                            "symbol": "AAPL",
                            "regularMarketPrice": Decimal("150.00"),
                            "regularMarketTime": "2025-04-27T10:00:00Z",
                        }
                    ]
                }
            },
        }
    )

    return table


@pytest.mark.integration
def test_get_stock_data(dynamodb_table):
    event = {
        "httpMethod": "GET",
        "path": "/stocks",
        "queryStringParameters": {"symbol": "AAPL"},
        "headers": {"Content-Type": "application/json"},
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["symbol"] == "AAPL"
    assert body["price"] == "150.00"


@pytest.mark.integration
def test_get_nonexistent_stock(dynamodb_table):
    event = {
        "httpMethod": "GET",
        "path": "/stocks",
        "queryStringParameters": {"symbol": "INVALID"},
        "headers": {"Content-Type": "application/json"},
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert "error" in body
