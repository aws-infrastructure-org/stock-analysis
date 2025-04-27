import json
import os
import yfinance as yf


def get_static_file(filename):
    # Get the absolute path to the static directory
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    file_path = os.path.join(static_dir, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            content_type = "text/html" if filename.endswith(".html") else "text/plain"
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": content_type,
                    "Access-Control-Allow-Origin": "*",
                },
                "body": content,
            }
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Debug logging
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"File not found: {filename}"}),
        }


def lambda_handler(event, context):
    try:
        path = event.get("path", "")

        # Serve the UI for root path
        if path == "/" or path == "":
            return get_static_file("stock_ui.html")

        # Handle API requests
        if path == "/api/stocks":
            params = event.get("queryStringParameters", {})
            if not params or "symbol" not in params:
                return {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": json.dumps({"error": "Symbol parameter is required"}),
                }

            symbol = params["symbol"]
            ticker = yf.Ticker(symbol)
            stock_info = ticker.info

            if not stock_info:
                return {
                    "statusCode": 404,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": json.dumps({"error": f"No data found for symbol {symbol}"}),
                }

            response_data = {
                "symbol": symbol,
                "price": str(stock_info.get("regularMarketPrice", 0)),
                "volume": stock_info.get("regularMarketVolume", 0),
                "data": stock_info,
            }

            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps(response_data),
            }

        # Handle unknown paths
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Not found"}),
        }

    except Exception as e:
        print(f"Error: {str(e)}")  # Debug logging
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }
