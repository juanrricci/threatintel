import json
from pprint import pprint

from src.predecode import predecode
from src.prematch import prematch
from src.decode import decode
from src.gatherDecoderFiles import gatherDecoderFiles


def main():
    decodersByFormat = gatherDecoderFiles()
    print('Format of decoders:\n')
    pprint(decodersByFormat)

    with open('logs.log') as logs:
        logNumber = 0
        for log in logs:
            logNumber += 1
            print('\n** LOG NUMERO', logNumber , '**')

            try:
                predecodedLog = predecode(log)
                print('\nVuelve del predecoder:')
                pprint(predecodedLog)

                chosenDecoderFilename = prematch(predecodedLog, decodersByFormat)
                print('\nPrematch result:', chosenDecoderFilename)

                fullDecodedLog = predecodedLog.copy()

                # decodedEvent = decode(predecodedLog, chosenDecoderFilename)
                # decodedlog = fullDecodedLog + decodedEvent
                fullDecodedLog['event'] = decode(predecodedLog, chosenDecoderFilename)
                
                pprint(fullDecodedLog)
                with open('output/normalized_decodification4.json', 'w') as normalizedDecodification:
                    json.dump(fullDecodedLog, normalizedDecodification, indent=4)

            except:
                print('\nINVALID LOG FORMAT')
                continue

if __name__ == '__main__':
    main()