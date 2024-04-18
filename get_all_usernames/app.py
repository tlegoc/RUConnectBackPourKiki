import boto3
import os
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['USER_TABLE'])

    user = table.scan()
    if user['ResponseMetadata']['HTTPStatusCode'] != 200:
        return {
            'statusCode': 500,
            'body': "Error retrieving user",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    data = user['Items']

    usernames = [u['username'] for u in data]

    return {
        'statusCode': 200,
        'body': json.dumps(usernames),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
