import json

def isJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True