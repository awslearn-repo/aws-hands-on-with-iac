import json
import boto3
import os

dynamodb = boto3.client('dynamodb')
table_name = os.environ['TABLE_NAME']

def handler(event, context):
    method = event['httpMethod']
    if method == 'POST':
        body = json.loads(event['body'])
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'id': {'S': body['id']},
                'timestamp': {'S': body['timestamp']},
                'message': {'S': body['message']}
            }
        )
        return {'statusCode': 200, 'body': json.dumps('Data saved')}
    elif method == 'GET':
        item_id = event['queryStringParameters']['id']
        result = dynamodb.get_item(
            TableName=table_name,
            Key={'id': {'S': item_id}}
        )
        return {'statusCode': 200, 'body': json.dumps(result.get('Item', {}))}
    else:
        return {'statusCode': 405, 'body': 'Method Not Allowed'}
