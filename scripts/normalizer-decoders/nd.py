import json
from pprint import pprint
from logDecoder import logDecode
import glob
import yaml

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

def main():
    prematchToDecoderFilenameList = parseAllDecoderFiles()
    # leer todos los yml y crear un diccionario
    # with open('ymlDir') as ymls:
    #   for yml in ymls:
    #     prematchDict[yml] = contenido del prematch del yml
    # prematch, yml
    # prematch_to_yml = has_field('win.system.providerName'), '000-Windows.yml'
    # prematch_to_yml = has_field('srcip'), '001-Suricata.yml'
    # prematchDict['prematch'] = [has_field('win.system.providerName'),has_field('win.system.providerGUID')]
    # prematchDict['decoder'] = '000-Windows.yml'

    # 1.) Iterate over logs.
    # 1.1) Iterate over decoders.
    # 1.1.1) Check if decoder has 'has_field' prematch and log is JSON.
    # 1.1.1.1) If True: check if field exists. If False: skip decoder.
    # 1.1.1.1.1) If True: decode.
    # 1.1.2) Check if decoder has 'regex' prematch and log is not JSON.
    # 1.1.2.1) If True: check if regex matches. If False: skip decode.
    # 1.1.2.1.1) If True: decode.

    with open('logs.log') as logs:
        for log in logs:
            logIsJSON = validateJSON(log)
            for prematchToDecoderFilename in prematchToDecoderFilenameList:
                prematchType = list(prematchToDecoderFilename['prematch'].keys())[0]
                if prematchType == 'has_field' and logIsJSON:
                    print('HAS FIELD and IS JSON')
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