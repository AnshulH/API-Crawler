import json

def getResponseJson(response):
    return json.loads(response.decode('utf-8'))
