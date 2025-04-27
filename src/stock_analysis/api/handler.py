import json
import os
import boto3


def lambda_handler(event, context):
    """
    Handle API Gateway requests for stock data
    """
    try:
        # Extract query parameters
        params = event.get('queryStringParameters', {})
        if not params or 'symbol' not in params:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Symbol parameter is required'})
            }

        symbol = params['symbol']
        
        # Get stock data from DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        
        response = table.query(
            KeyConditionExpression='symbol = :sym',
            ExpressionAttributeValues={':sym': symbol},
            Limit=1,
            ScanIndexForward=False  # Get most recent first
        )
        
        if not response['Items']:
            error_msg = {'error': f'No data found for symbol {symbol}'}
            return {
                'statusCode': 404,
                'body': json.dumps(error_msg)
            }
            
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'][0])
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
