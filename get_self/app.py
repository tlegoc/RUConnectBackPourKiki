import boto3
import os
import jwt
import json

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

    data = user['Item']

    # Is a string set, so we convert to a list that can be converted to json
    data['pendingfriends'] = list(data['pendingfriends'])
    data['pendingfriends'].remove("")
    data['requestsfriends'] = list(data['requestsfriends'])
    data['requestsfriends'].remove("")
    data['friends'] = list(data['friends'])
    data['friends'].remove("")
    data['friendsstatus'] = {}

    # Get all users, filter to get only friends and then map their username to their status
    users = table.scan()
    for user in users['Items']:
        if user['username'] in data['friends']:
            data['friendsstatus'][user['username']] = user['status']

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
