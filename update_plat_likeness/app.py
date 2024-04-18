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

    feel = event["queryStringParameters"]['feel']
    plat = event["queryStringParameters"]['plat']

    if feel == "like":
        pass
    elif feel == "dislike":
        pass
    else:
        return {
            'statusCode': 400,
            'body': "feel field has an incorrect value: should be [like, dislike]"
        }

    # Delete
    table.update_item(
        Key={
            'username': username
        },
        UpdateExpression='SET #plats_feel.#plat = :f',
        ExpressionAttributeNames={
            '#plats_feel': 'plats_feel',
            '#plat': plat
        },
        ExpressionAttributeValues={
            ':f': feel,
        },
    )

    return {
        'statusCode': 200,
        'body': "",
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
