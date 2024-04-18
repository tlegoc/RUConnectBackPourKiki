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

    # if "queryStringParameters" not in event or event["queryStringParameters"] is None:
    friend_name = event["queryStringParameters"]['friend_name']

    friend_exists = table.get_item(
        Key={
            'username': friend_name
        }
    )

    if 'Item' not in friend_exists:
        return {
            'statusCode': 400,
            'body': "Friend does not exist"
        }

    table.update_item(
        Key={
            'username': username
        },
        UpdateExpression='ADD friends :user',
        ExpressionAttributeValues={
            ':user': set([friend_name]),
        },
    )

    table.update_item(
        Key={
            'username': friend_name
        },
        UpdateExpression='ADD friends :user',
        ExpressionAttributeValues={
            ':user': set([username]),
        },
    )

    return {
        'statusCode': 200,
        'body': "",
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
