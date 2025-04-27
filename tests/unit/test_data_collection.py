import json
from unittest.mock import patch, MagicMock
from stock_analysis.collectors.data_collection import lambda_handler


@patch('boto3.client')
@patch('boto3.resource')
@patch('yfinance.Ticker')
def test_lambda_handler(mock_ticker, mock_boto3_client, mock_boto3_resource):
    mock_stock_data = {
        'quoteResponse': {
            'result': [{
                'symbol': 'AAPL',
                'regularMarketPrice': 150.00,
                'regularMarketTime': '2025-04-27T10:00:00Z'
            }]
        }
    }
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.json.return_value = mock_stock_data
    mock_response.status_code = 200
    mock_ticker.return_value = mock_response
    
    # Mock S3
    mock_s3 = MagicMock()
    mock_boto3_client.return_value = mock_s3
    
    # Mock DynamoDB
    mock_table = MagicMock()
    mock_boto3_resource.return_value = MagicMock()
    mock_boto3_resource.return_value.Table.return_value = mock_table
    
    lambda_event = {
        "Records": [{
            "Sns": {
                "Message": json.dumps({"symbol": "AAPL"})
            }
        }]
    }
    
    response = lambda_handler(lambda_event, None)
    
    assert response['statusCode'] == 200
    assert 'Successfully collected data' in response['body']
    
    # Verify S3 put_object was called
    mock_s3.put_object.assert_called_once()
    
    # Verify DynamoDB put_item was called
    mock_table.put_item.assert_called_once()


@patch('requests.get')
def test_data_collection_api_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    lambda_event = {
        "Records": [{
            "Sns": {
                "Message": json.dumps({"symbol": "AAPL"})
            }
        }]
    }
    
    response = lambda_handler(lambda_event, None)
    
    assert response['statusCode'] == 500
    assert 'Failed to collect data' in response['body']