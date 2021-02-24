import json
import yaml
import re
from benedict import benedict
from pprint import pprint

def JSONProcessSet(decodedLog, setList, benedictedLog):
    print('\nJSON setList:', setList)
    for set in setList:
        try:
            decodedLog[set['destination']] = benedictedLog[set['original']]
        except:
            continue
    return True

def JSONProcessParse(decodedLog, parseList, benedictedLog):
    print('\nJSON parseList:', parseList)
    for parse in parseList:
        try:
            # print('benedicted original:', benedictedLog[processor['original']])
            m = re.search(parse['regex'], benedictedLog[parse['original']])
            # print('m:', m.groups())
            n = re.search('\.(?P<hash>\w+)$', parse['destination'])
            decodedLog[parse['destination']] = m.group(n.group('hash'))
        except:
            continue        
    return True

def JSONProcessResolve(decodedLog, resolveList, benedictedLog):
    print('\nJSON resolveList:', resolveList)
    return True


def decodeJSON(predecodedLog, chosenDecoderFilename):
    processorFunctions = {
        'set': JSONProcessSet,
        'parse': JSONProcessParse,
        'resolve': JSONProcessResolve
    }

    processorKeys = list(processorFunctions.keys())
    print('ProcessorKeys:', processorKeys)

    processorDict = {key : [] for key in processorKeys}
    print('ProcessorDict:', processorDict)

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
            for processor in event['event']['processors']:
                for processorType in processorKeys:  
                    if processorType in processor: processorDict[processorType].append(processor)
                    
            print('ProcessorDict:', processorDict)

            for processorType in processorKeys:
                processorFunctions.get(processorType, 'Invalid function key')(decodedLog, processorDict[processorType], benedictedLog)
            
                    # if 'set' in processor and processor['set'] == None:
                    #     try:
                    #         decodedLog[processor['destination']] = benedictedLog[processor['original']]
                    #     except:
                    #         continue

                    # elif 'parse' in processor and processor['parse'] == None:
                    #     try:
                    #         # print('benedicted original:', benedictedLog[processor['original']])
                    #         m = re.search(processor['regex'], benedictedLog[processor['original']])
                    #         # print('m:', m.groups())
                    #         n = re.search('\.(?P<hash>\w+)$', processor['destination'])
                    #         decodedLog[processor['destination']] = m.group(n.group('hash'))
                    #     except:
                    #         continue

                    # elif 'resolve' in processor and processor['resolve'] == None:
                    #     try:   
                    #         decodedLog[processor['destination']] = benedictedLog[processor['original']]
                    #     except:
                    #         continue

    return decodedLog

def plaintextProcessRegex(decodedLog, regexList, rawLog):
    print('\nregexList:', regexList)
    for regex in regexList:
        regexResult = re.search(regex['regex'], rawLog)
        # if True:
        try:
            regexResultKeyValues = regexResult.groupdict()
            # print('\nREGEX:', regexResultKeyValues)
            regexResultKeys = list(regexResultKeyValues.keys())
            # print(regexResultKeys)
            dot = re.compile('__')
            for regexKey in regexResultKeys:
                newRegexResultKey = dot.sub('.', regexKey)
                # print('\nnewRegexResultKey:', newRegexResultKey)
                decodedLog[newRegexResultKey] = regexResultKeyValues[regexKey]
        except:
            continue
    return True

def plaintextProcessSet(decodedLog, setList, rawLog):
    print('\nsetList:', setList)
    return True

def plaintextProcessResolve(decodedLog, resolveList, rawLog):
    print('\nresolveList:', resolveList)
    return True


def decodePlaintext(predecodedLog, chosenDecoderFilename):
    processorFunctions = {
        'regex': plaintextProcessRegex,
        'set': plaintextProcessSet,
        'resolve': plaintextProcessResolve
    }

    processorKeys = list(processorFunctions.keys())
    print('ProcessorKeys:', processorKeys)

    processorDict = {key : [] for key in processorKeys}
    print('ProcessorDict:', processorDict)

    decodedLog = benedict()
    decodedLog['agent'] = predecodedLog['agent']
    decodedLog['event.original'] = predecodedLog['log']['raw']

    with open(chosenDecoderFilename) as decoderFileOpened: 
        decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)
        decodedLog[decoderDict['vendor']] = {}
        decodedLog[decoderDict['vendor']][decoderDict['component']] = predecodedLog['log']['raw']

        for event in decoderDict['events']:
            print('\nEVENT*:', event)
            if re.search(event['event']['match'], predecodedLog['log']['raw']):
                print('\nMatched event:', event['event']['id'], event['event']['description'])
                for processor in event['event']['processors']:
                    for processorType in processorKeys:
                        if processorType in processor: processorDict[processorType].append(processor)
                    # if 'regex' in processor:
                    #     processorDict['regex'].append(processor['regex'])

                    #     # regex_group = re.match(processor['regex'], predecodedLog['log']['raw'])
                        

                    # elif 'set' in processor and processor['set'] == None: processorDict['set'].append({'original': processor['original'], 'destination': processor['destination']})
                    #     # try:
                    #     #     decodedLog[processor['destination']] = regex_group.group(processor['original'])
                    #     # except:
                    #     #     continue
                        
                    # elif 'resolve' in processor and processor['resolve'] == None: processorDict['resolve'].append({'original': processor['original'], 'destination': processor['destination']})

                print('ProcessorDict:', processorDict)

                for processorType in processorKeys:
                    processorFunctions.get(processorType, 'Invalid function key')(decodedLog, processorDict[processorType], predecodedLog['log']['raw'])
            
            else: print('\nSkipped event:', event['event']['id'], event['event']['description'])

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
