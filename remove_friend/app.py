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

    # plat = parse.unquote(event['pathParameters']['plat'])

    if event['body'] is None:
        return {
            'statusCode': 400,
            'body': "Body must not be empty"
        }


    body = json.loads(event['body'])

    if "user" not in body:
        return {
            'statusCode': 400,
            'body': "field [feel] doesn't exists"
        }

    # Delete
    table.update_item(
        Key={
            'username': username
        },
        UpdateExpression='DELETE friends :user',
        ExpressionAttributeValues={
            ':user': set([body['user']]),
        },
    )

    return {
        'statusCode': 200,
        'body': "",
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
