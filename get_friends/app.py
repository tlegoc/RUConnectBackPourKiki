import boto3
import json
import os
import jwt
from urllib import parse


def lambda_handler(event, context):
    token = jwt.decode(event['headers']['Authorization'].replace('Bearer ', ''), algorithms=['RS256'],
                       options={"verify_signature": False})

    username = token['cognito:username']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['USER_TABLE'])

    user = table.get_item(Key={'username': username})
    if user['ResponseMetadata']['HTTPStatusCode'] != 200:
        return {
            'statusCode': 500,
            'body': "Error retrieving user",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    user = user["Item"]

    data = {}
    data['pendingfriends'] = list(user['pendingfriends'])
    data['requestsfriends'] = list(user['requestsfriends'])
    data['friends'] = list(user['friends'])

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
