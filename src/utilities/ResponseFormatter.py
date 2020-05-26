import json

# Returns json response from given json string
def getResponseJson(response):
    return json.loads(response.decode('utf-8'))
