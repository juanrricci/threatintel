import json
from pprint import pprint
from logDecoder import logDecode
import glob
import yaml
import re
from benedict import benedict

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def parseAllDecoderFiles():
    decoderFiles = glob.glob('decoders/*.yml')
    prematchToDecoderFilenameList = []
    for decoderFile in decoderFiles:
        with open(decoderFile) as decoderFileOpened: 
            decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)
            pprint(decoderDict)
            prematchToDecoderFilenameList.append({'prematch': decoderDict['prematch'], 'filename': decoderFile})
    print(prematchToDecoderFilenameList)
    # print(list(prematchToDecoderFilenameList[0]['prematch'].keys()))
    return prematchToDecoderFilenameList

def existFields(jsonLog, prematchFields):
    # print('JSON Log:', jsonLog)
    for prematchField in prematchFields:
        # print('Prematch field:', prematchField)
        # p = re.compile('\w+')
        # m = p.findall(prematchField)
        # print('Groups:', m)
        # return True if jsonLog[m[0]][m[1]][m[2]] else False
        benedictedLog = benedict(jsonLog)
        # print('Benedicted log:', benedictedLog)
        if not prematchField in benedictedLog:
            print('Prematch field', prematchField, 'not found.')
            return False
        else: print('Prematch field', prematchField, 'found. OK.')
    return True

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
                        dictOutput[processor['destination']] = benedictedLog[processor['original']]
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


def main():
    prematchToDecoderFilenameList = parseAllDecoderFiles()

    # - Iterate over logs.
    # -- Iterate over decoders.
    # --- Check if decoder has 'has_field' prematch and log is JSON.
    # ---- If True: check if field exists. If False: skip decoder.
    # ----- If True: decode.
    # --- Check if decoder has 'regex' prematch and log is not JSON.
    # ---- If True: check if regex matches. If False: skip decode.
    # ----- If True: decode.

    with open('logs.log') as logs:
        for log in logs:
            logIsJSON = validateJSON(log)
            jsonLog = json.loads(log) if logIsJSON else False
            for prematchToDecoderFilename in prematchToDecoderFilenameList:
                prematchType = list(prematchToDecoderFilename['prematch'].keys())[0]
                decoderFilename = prematchToDecoderFilename['filename']
                print(decoderFilename)
                # decoderFilename = 
                if prematchType == 'has_field' and logIsJSON:
                    print('HAS FIELD and IS JSON')
                    # print('Do fields exist?',existFields(jsonLog, prematchToDecoderFilename['prematch']['has_field']))
                    if existFields(jsonLog, prematchToDecoderFilename['prematch']['has_field']):
                        createJsonOutput(jsonLog, decoderFilename)
                elif prematchType == 'regex' and not logIsJSON:
                    print('REGEX and IS NOT JSON')
                else:
                    print('Exception:')
                    print('Prematch Type:', prematchType)
                    print('Log is JSON:', logIsJSON)
            #     if prematchToDecoderFilename['prematch'] in jsonLog:
            #         decodedEvent = logDecode(log, prematchToDecoderFilename['filename'])
            #         pprint(decodedEvent)
            # # for i in prematch_to_yml:
            # #   case i['has_field']:  
            # #     logNormalizer(i['yaml'],log)
            # #   case i['regex']:
            # #     logNormalizer(i['yaml'],log)
            # if validateJSON(log):
            #     # This is a JSON-formatted log
            #     print('Valid JSON log.')
            #     jsonLog = json.loads(log)
            # else:
            #     # Assume this is a syslog log
            #     print('Valid Syslog log.')

if __name__ == '__main__':
    main()