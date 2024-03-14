import boto3
import os


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['USER_TABLE'])

    response = table.put_item(
        Item={
            'username': event['userName'],
            "friends": set(["DummyFriend"]),
            "plats_feel": {}
        }
    )

    return event
