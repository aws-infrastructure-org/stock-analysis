import json
from unittest.mock import patch, MagicMock
from decimal import Decimal
from stock_analysis.api.handler import lambda_handler


@patch('boto3.client')
@patch('boto3.resource')
def test_lambda_handler(mock_boto3_resource, mock_boto3_client):
    # Create event
    event = {
        "httpMethod": "GET",
        "path": "/stocks",
        "queryStringParameters": {"symbol": "AAPL"},
        "headers": {
            "Content-Type": "application/json"
        }
    }

    # Create mock table
    mock_table = MagicMock()
    mock_boto3_resource.return_value = MagicMock()
    mock_boto3_resource.return_value.Table.return_value = mock_table
    
    # Mock DynamoDB query response
    mock_table.query.return_value = {
        'Items': [{
            'symbol': 'AAPL',
            'timestamp': '2025-04-27T10:00:00Z',
            'price': '150.00',
            'data': {
                'quoteResponse': {
                    'result': [{
                        'symbol': 'AAPL',
                        'regularMarketPrice': Decimal('150.00'),
                        'regularMarketTime': '2025-04-27T10:00:00Z'
                    }]
                }
            }
        }]
    }
    
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['symbol'] == 'AAPL'
    mock_table.query.assert_called_once()


@patch('boto3.client')
@patch('boto3.resource')
def test_lambda_handler_missing_symbol(mock_boto3_resource, mock_boto3_client):
    event = {
        "httpMethod": "GET",
        "path": "/stocks",
        "queryStringParameters": {},
        "headers": {
            "Content-Type": "application/json"
        }
    }
    
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'error' in body