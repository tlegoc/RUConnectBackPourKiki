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

    if "action" not in event["queryStringParameters"]:
        return {
            'statusCode': 200,
            'body': json.dumps(list(user["friends"])),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    action = event["queryStringParameters"]['action']

    if action != "add" and action != "remove" and action != "accept":
        return {
            'statusCode': 500,
            'body': "Error, action is unknown",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }


    if "friendname" not in event["queryStringParameters"]:
        return {
            'statusCode': 500,
            'body': "Error, no friend name provided",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    friendname = event["queryStringParameters"]["friendname"]

    if friendname == username:
        return {
            'statusCode': 500,
            'body': "Error, cannot add yourself as a friend",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    friend_exists = table.get_item(
        Key={
            'username': friendname
        }
    )

    if 'Item' not in friend_exists:
        return {
            'statusCode': 500,
            'body': "Friend does not exist"
        }

    friend = friend_exists["Item"]

    if action == "add":
        if username in friend["pendingfriends"] or username in friend["requestsfriends"] or username in friend["friends"]:
            print("Already friend")
            return {
                'statusCode': 500,
                'body': "You are already friend, or a request is pending"
            }

        if friendname in user["pendingfriends"] or friendname in user["requestsfriends"] or friendname in user["friends"]:
            return {
                'statusCode': 400,
                'body': "You are already friend, or a request is pending"
            }

        print("Updating user")
        table.update_item(
            Key={
                'username': username
            },
            UpdateExpression='ADD pendingfriends :f',
            ExpressionAttributeValues={
                ':f': set([friendname]),
            },
        )

        table.update_item(
            Key={
                'username': friendname
            },
            UpdateExpression='ADD requestsfriends :f',
            ExpressionAttributeValues={
                ':f': set([username]),
            },
        )

        return {
            'statusCode': 200,
            'body': "",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    if action == "remove":
        if (username not in friend["pendingfriends"]) and (username not in friend["requestsfriends"]) and (username not in friend["friends"]):
            return {
                'statusCode': 400,
                'body': "Cannot remove friend, not a friend or no request is pending",
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                }
            }

        if (friendname not in user["pendingfriends"]) and (friendname not in user["requestsfriends"]) and (friendname not in user["friends"]):
            return {
                'statusCode': 400,
                'body': "Cannot remove friend, not a friend or no request is pending",
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                }
            }

        expr = ""
        if username in friend["pendingfriends"]:
            expr = 'DELETE pendingfriends :f'
        elif username in friend["requestsfriends"]:
            expr = 'DELETE requestsfriends :f'
        elif username in friend["friends"]:
            expr = 'DELETE friends :f'

        table.update_item(
            Key={
                'username': friendname
            },
            UpdateExpression=expr,
            ExpressionAttributeValues={
                ':f': set([username]),
            },
        )

        expr2 = ""
        if friendname in user["pendingfriends"]:
            expr2 = 'DELETE pendingfriends :f'
        elif friendname in user["requestsfriends"]:
            expr2 = 'DELETE requestsfriends :f'
        elif friendname in user["friends"]:
            expr2 = 'DELETE friends :f'

        table.update_item(
            Key={
                'username': username
            },
            UpdateExpression=expr2,
            ExpressionAttributeValues={
                ':f': set([friendname]),
            },
        )

        return {
            'statusCode': 200,
            'body': "",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    if action == "accept":
        print("Accepting friend")
        if username not in friend["pendingfriends"]:
            return {
                'statusCode': 400,
                'body': "You are already friend, or no request is pending",
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                }
            }

        if friendname not in user["requestsfriends"]:
            return {
                'statusCode': 400,
                'body': "You are already friend, or no request is pending",
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                }
            }

        table.update_item(
            Key={
                'username': username
            },
            UpdateExpression='DELETE requestsfriends :f ADD friends :f',
            ExpressionAttributeValues={
                ':f': set([friendname]),
            },
        )

        table.update_item(
            Key={
                'username': friendname
            },
            UpdateExpression='DELETE pendingfriends :f ADD friends :f',
            ExpressionAttributeValues={
                ':f': set([username]),
            },
        )

        return {
            'statusCode': 200,
            'body': "",
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
