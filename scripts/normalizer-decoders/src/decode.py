import json
import yaml
import re
from benedict import benedict
from pprint import pprint

def JSONProcessSet(decodedLog, setList, benedictedLog):
    print('\nJSON setList:', setList)
    extracted = benedict()
    for set in setList:
        if True:
        # if 'wcs_origin' in set:
            # if True:
            if set['wcs_origin'] == 'normalized':
                try:
                    decodedLog[set['destination']] = benedictedLog[set['original']]
                except:
                    continue
            elif set['wcs_origin'] == 'extracted':
                try:
                    extracted[set['destination']] = benedictedLog[set['original']]
                except:
                    continue
        # else:
        #     try:
        #         decodedLog[set['destination']] = benedictedLog[set['original']]
        #     except:
        #         continue
    print('\nEXTRACTED: ', extracted)
    decodedLog['extracted'] = extracted
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

    # Create some auxiliar structures that help with execution of decoder processors later
    processorKeys = list(processorFunctions.keys())
    print('ProcessorKeys:', processorKeys)

    processorDict = {key : [] for key in processorKeys}
    print('ProcessorDict:', processorDict)

    decodedLog = benedict()
    # Add agent meta information
    decodedLog['agent'] = predecodedLog['agent']
    # Add raw log under event.original field
    decodedLog['event.original'] = predecodedLog['log']['raw']

    with open(chosenDecoderFilename) as decoderFileOpened: 
        # "Benedict" the raw log for applying processors on it later
        benedictedLog = benedict(predecodedLog['log']['raw'])
        # Load the YAML decoder
        decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)

        # Load the JSON raw log for adding it under vendor_value.module_value keys
        rawToJSON = json.loads(predecodedLog['log']['raw'])
        decodedLog[decoderDict['vendor']] = {}
        decodedLog[decoderDict['vendor']][decoderDict['module']] = rawToJSON

        # Look for the processor type of each processor for executing the proper function
        for event in decoderDict['events']:
            for processor in event['event']['processors']:
                for processorType in processorKeys:  
                    if processorType in processor: processorDict[processorType].append(processor)
                    
            print('ProcessorDict:', processorDict)

            for processorType in processorKeys:
                processorFunctions.get(processorType, 'Invalid function key')(decodedLog, processorDict[processorType], benedictedLog)

    return decodedLog

def plaintextProcessRegex(decodedLog, regexList, rawLog):
    print('\nregexList:', regexList)
    for regex in regexList:
        # replace(regex['regex'], ., __)
        double_underscore = re.compile('\.')
        validFormatRegex = double_underscore.sub('__', regex['regex'])
        regexResult = re.search(validFormatRegex, rawLog)
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
        decodedLog[decoderDict['vendor']][decoderDict['module']] = predecodedLog['log']['raw']

        for event in decoderDict['events']:
            print('\nEVENT*:', event)
            if re.search(event['event']['match'], predecodedLog['log']['raw']):
                print('\nMatched event:', event['event']['id'], event['event']['description'])
                for processor in event['event']['processors']:
                    for processorType in processorKeys:
                        if processorType in processor: processorDict[processorType].append(processor)

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
