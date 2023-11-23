import boto3, json

def lambda_handler(event, context):
    print('EVENT:')
    print(event)

    if event['RequestType'] == "Create":
        pass

    return {
        'statusCode': 200,
        'body': "You're not supposed to be here!"
    }