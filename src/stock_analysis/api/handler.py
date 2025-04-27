import json
import os
import boto3
import base64
import mimetypes
from pathlib import Path

def get_static_file(path):
    """Helper function to read and return static files"""
    try:
        # Get the absolute path to the static directory
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        file_path = os.path.join(static_dir, path.lstrip('/'))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            with open(file_path, 'rb') as f:
                content = f.read()
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': content_type,
                    'Access-Control-Allow-Origin': '*'
                },
                'body': base64.b64encode(content).decode('utf-8'),
                'isBase64Encoded': True
            }
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'File not found'}),
            'headers': {'Access-Control-Allow-Origin': '*'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Access-Control-Allow-Origin': '*'}
        }

def lambda_handler(event, context):
    """
    Handle API Gateway requests for stock data and static files
    """
    try:
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            }

        path = event.get('path', '')
        
        # Serve the UI for root path
        if path == '/' or path == '':
            return get_static_file('stock_ui.html')
            
        # Serve static files
        if path.startswith('/static/'):
            return get_static_file(path[8:])  # Remove /static/ prefix

        # Handle API requests
        if path == '/api/stocks':
            params = event.get('queryStringParameters', {})
            if not params or 'symbol' not in params:
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'Symbol parameter is required'})
                }

            symbol = params['symbol']
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(os.environ['TABLE_NAME'])

            response = table.query(
                KeyConditionExpression='symbol = :sym',
                ExpressionAttributeValues={':sym': symbol},
                Limit=1,
                ScanIndexForward=False  # Get most recent first
            )

            if not response['Items']:
                return {
                    'statusCode': 404,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': f'No data found for symbol {symbol}'})
                }

            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(response['Items'][0])
            }

        # Handle unknown paths
        return {
            'statusCode': 404,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Not found'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
