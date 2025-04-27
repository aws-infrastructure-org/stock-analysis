import json
import os
import boto3
import yfinance as yf
from datetime import datetime, UTC


def lambda_handler(event, context):
    """
    Collect stock data from Yahoo Finance API and store in S3/DynamoDB
    """
    try:
        # Parse SNS message
        records = event.get('Records', [])
        if not records:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No records in event'})
            }
            
        message = json.loads(records[0]['Sns']['Message'])
        symbol = message.get('symbol')
        
        if not symbol:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No symbol provided'})
            }
            
        # Get stock data
        ticker = yf.Ticker(symbol)
        stock_info = ticker.info
        
        if not stock_info:
            error_msg = {'error': f'Failed to get data for {symbol}'}
            return {
                'statusCode': 500,
                'body': json.dumps(error_msg)
            }
            
        # Store raw data in S3
        timestamp = datetime.now(UTC).isoformat()
        s3 = boto3.client('s3')
        
        s3.put_object(
            Bucket=os.environ['BUCKET_NAME'],
            Key=f'{symbol}/{timestamp}.json',
            Body=json.dumps(stock_info)
        )
        
        # Store processed data in DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        
        table.put_item(Item={
            'symbol': symbol,
            'timestamp': timestamp,
            'price': str(stock_info.get('regularMarketPrice', 0)),
            'volume': stock_info.get('regularMarketVolume', 0),
            'data': stock_info
        })
        
        success_msg = {'message': f'Successfully collected data for {symbol}'}
        return {
            'statusCode': 200,
            'body': json.dumps(success_msg)
        }
        
    except Exception as e:
        error_msg = {'error': f'Failed to collect data: {str(e)}'}
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
