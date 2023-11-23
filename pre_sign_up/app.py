import re

def lambda_handler(event, context):
    if not re.match(r'^[A-Za-z_\-0-9.]+$', event['userName']):
        raise Exception("Pseudo incorrect. Sont autorisés : Lettres, chiffres, \"_\" et\"-\"")

    event['response']['autoConfirmUser'] = True

    if 'email' in event['request']['userAttributes']:
        event['response']['autoVerifyEmail'] = True

    if 'phone_number' in event['request']['userAttributes']:
        event['response']['autoVerifyPhone'] = True

    return event