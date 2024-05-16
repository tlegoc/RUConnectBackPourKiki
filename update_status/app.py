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

    status = event["queryStringParameters"]['status']

    if status == "inside":
        pass
    elif status == "inqueue":
        pass
    elif status == "out":
        pass
    else:
        return {
            'statusCode': 400,
            'body': "status field has an incorrect value: should be [inside, inqueue, out]"
        }


    # Delete
    table.update_item(
        Key={
            'username': username
        },
        UpdateExpression='SET #status = :f',
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':f': status,
        },
    )

    return {
        'statusCode': 200,
        'body': "",
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
