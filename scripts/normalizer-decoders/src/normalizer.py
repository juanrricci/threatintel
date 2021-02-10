import yaml
import re

from benedict import benedict

def createJsonOutput(jsonLog, decoderFilename):
    dictOutput = benedict()
    with open(decoderFilename) as decoderFileOpened: 
        benedictedLog = benedict(jsonLog)
        decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)
        for event in decoderDict['events']:
            print('EVENT:', event)
            for processor in event['event']['processors']:  
                print('PROCESSOR', processor)  
                if 'set' in processor and processor['set'] == None:
                    try:
                        dictOutput[processor['destination']] = benedictedLog[processor['original']]
                    except:
                        continue
                elif 'parse' in processor and processor['parse'] == None:
                    try:
                        # print('benedicted original:', benedictedLog[processor['original']])
                        m = re.search(processor['regex'], benedictedLog[processor['original']])
                        print('m:', m.groups())
                        n = re.search('\.(?P<hash>\w+)$', processor['destination'])
                        dictOutput[processor['destination']] = m.group(n.group('hash'))
                    except:
                        continue
                elif 'resolve' in processor and processor['resolve'] == None:
                    try:   
                        dictOutput[processor['destination']] = benedictedLog[processor['original']]
                    except:
                        continue
    print(dictOutput)
    with open('normalized_decodification2.json', 'w') as normalizedDecodification:
        json.dump(dictOutput, normalizedDecodification, indent=4) 
