import json
from unittest.mock import patch, MagicMock
from stock_analysis.api.handler import lambda_handler


@patch("yfinance.Ticker")
def test_lambda_handler(mock_ticker):
    # Create event
    event = {
        "httpMethod": "GET",
        "path": "/api/stocks",
        "queryStringParameters": {"symbol": "AAPL"},
        "headers": {"Content-Type": "application/json"},
    }

    # Mock yfinance response
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.info = {
        "symbol": "AAPL",
        "regularMarketPrice": 150.00,
        "regularMarketVolume": 1000000,
        "marketCap": 2500000000000,
        "longBusinessSummary": "Apple Inc."
    }
    mock_ticker.return_value = mock_ticker_instance

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["symbol"] == "AAPL"
    assert float(body["price"]) == 150.00


@patch("yfinance.Ticker")
def test_lambda_handler_missing_symbol(mock_ticker):
    event = {
        "httpMethod": "GET",
        "path": "/api/stocks",
        "queryStringParameters": {},
        "headers": {"Content-Type": "application/json"},
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "error" in body
