def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': "You're not supposed to be here!",
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }