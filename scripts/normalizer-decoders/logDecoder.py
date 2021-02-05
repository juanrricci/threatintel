import yaml
import json
from pprint import pprint

def logDecode(log):
    rawLog = log
    jsonLog = json.loads(log)
    # print(json.dumps(jsonLog, indent=4)) 

    decodedEvent = {}

    with open('000-Windows.yml') as windowsDecoderFile:
    # if fields ~= match(mapping, log):
    #   for field in fields:
    #     fields[field]
    #  
        decodedEvent = yaml.load(windowsDecoderFile, Loader=yaml.FullLoader)
        pprint(decodedEvent)
        decodedEvent['mapping']['timestamp'] = jsonLog['win']['eventdata']['utcTime']
        decodedEvent['mapping']['channel'] = jsonLog['win']['system']['channel']
        decodedEvent['mapping']['hostname'] = jsonLog['win']['system']['computer']
        decodedEvent['mapping']['event-id'] = jsonLog['win']['system']['eventID']
        decodedEvent['mapping']['severity'] = jsonLog['win']['system']['severityValue']
        # decodedEvent['mapping']['message'] = jsonLog['win']['system']['message']
        # decodedEvent['mapping']['full-log'] = rawLog

    return decodedEvent
