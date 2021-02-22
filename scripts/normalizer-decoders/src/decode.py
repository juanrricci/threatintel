import json
import yaml
import re
from benedict import benedict
from pprint import pprint


def decodeJSON(predecodedLog, chosenDecoderFilename):
    decodedLog = benedict()
    decodedLog['agent'] = predecodedLog['agent']
    decodedLog['event.original'] = predecodedLog['log']['raw']

    with open(chosenDecoderFilename) as decoderFileOpened: 
        benedictedLog = benedict(predecodedLog['log']['raw'])
        decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)

        # decodedLog[decoderDict['vendor']][decoderDict['component']] = json.loads(predecodedLog['log']['raw'])
        rawToJSON = json.loads(predecodedLog['log']['raw'])
        decodedLog[decoderDict['vendor']] = {}
        decodedLog[decoderDict['vendor']][decoderDict['component']] = rawToJSON

        for event in decoderDict['events']:
            # print('\nEVENT:')
            # pprint(event)

            for processor in event['event']['processors']:  
                # print('PROCESSOR', processor)  

                if 'set' in processor and processor['set'] == None:
                    try:
                        decodedLog[processor['destination']] = benedictedLog[processor['original']]
                    except:
                        continue

                elif 'parse' in processor and processor['parse'] == None:
                    try:
                        # print('benedicted original:', benedictedLog[processor['original']])
                        m = re.search(processor['regex'], benedictedLog[processor['original']])
                        # print('m:', m.groups())
                        n = re.search('\.(?P<hash>\w+)$', processor['destination'])
                        decodedLog[processor['destination']] = m.group(n.group('hash'))
                    except:
                        continue

                elif 'resolve' in processor and processor['resolve'] == None:
                    try:   
                        decodedLog[processor['destination']] = benedictedLog[processor['original']]
                    except:
                        continue

    return decodedLog



def decodePlaintext(predecodedLog, chosenDecoderFilename):
    decodedLog = benedict()
    decodedLog['agent'] = predecodedLog['agent']
    decodedLog['event.original'] = predecodedLog['log']['raw']

    with open(chosenDecoderFilename) as decoderFileOpened: 
        # benedictedLog = benedict(predecodedLog['log']['raw'])
        decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)

        # decodedLog[decoderDict['vendor']][decoderDict['component']] = json.loads(predecodedLog['log']['raw'])
        # rawToJSON = json.loads(predecodedLog['log']['raw'])
        decodedLog[decoderDict['vendor']] = {}
        decodedLog[decoderDict['vendor']][decoderDict['component']] = predecodedLog['log']['raw']

        for event in decoderDict['events']:
            # print('\nEVENT:')
            # pprint(event)
            regex_group = {}
            for processor in event['event']['processors']:
                # print('PROCESSOR', processor)  


                if 'regex' in processor:
                    regex_group = re.match(processor['regex'], predecodedLog['log']['raw'])

                elif 'set' in processor and processor['set'] == None:
                    try:
                        decodedLog[processor['destination']] = regex_group.group(processor['original'])
                    except:
                        continue

    return decodedLog


def decodeXML(predecodedLog, chosenDecoderFilename):
    return True

def decode(predecodedLog, chosenDecoderFilename):
    decoderType = {
        'json': decodeJSON,
        'plaintext': decodePlaintext,
        'xml': decodeXML
    }

    return decoderType.get(predecodedLog['log']['type'], 'Invalid log type')(predecodedLog, chosenDecoderFilename)
