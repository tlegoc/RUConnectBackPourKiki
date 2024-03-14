from urllib import parse
import requests
import json

def lambda_handler(event, context):
    ville = parse.unquote(event['pathParameters']['ville'])
    if "body" not in event or event["body"] is None:
        data = requests.get("http://webservices-v2.crous-mobile.fr:8080/feed/{ville}/externe/menu.xml".format(ville=ville))
    else:
        # print(event['body'])
        body = json.loads(event['body'])

        if "get_ids" in body and bool(body["get_ids"]):
            data = requests.get("http://webservices-v2.crous-mobile.fr/feed/{ville}/externe/resto.xml".format(ville=ville))
        else:
            data = requests.get("http://webservices-v2.crous-mobile.fr:8080/feed/{ville}/externe/menu.xml".format(ville=ville))

    return {
        'statusCode': data.status_code,
        'headers': {
            'Content-Type': data.headers['Content-Type'],
            'Access-Control-Allow-Origin': '*'
        },
        'body': data.content
    }
