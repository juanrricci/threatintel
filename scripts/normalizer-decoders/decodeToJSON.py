# This program reads log lines from an input file, decodes the information
# from these logs and writes that information in normalized fields inside
# JSON objects.
# Each JSON object is stringified and written in an output file.

import json
from pprint import pprint

from src.fetchDecoders import fetchDecoders
from src.predecode import predecode
from src.prematch import prematch
from src.decode import decode

def main():
    # Paths of YML decoder files are fetched and added to a dictionary which
    # classifies them by log format. Prematch options are included along with
    # decoder file paths.
    decodersByFormat = fetchDecoders()
    print('Format of decoders:\n')
    pprint(decodersByFormat)

    with open('logs.log') as logs:
        logNumber = 0
        for log in logs:
            logNumber += 1
            print('\n** LOG #', logNumber , '**')
            print('\nLog:', log)
            # if True:
            try:
                # Read logs are predecoded for extracting context information.
                predecodedLog = predecode(log)
                print('\nPredecoded log:')
                pprint(predecodedLog)

                # Predecoded logs are prematched for finding the right decoder.
                chosenDecoderFilename = prematch(predecodedLog, decodersByFormat)
                print('\nPrematch result:', chosenDecoderFilename)

                # Once the right decoder is found, the log information is decoded
                # and stored in normalized fields.
                # if chosenDecoderFilename:
                #     decodedLog = decode(predecodedLog, chosenDecoderFilename)
                #     print('\nDecoded log:')
                #     pprint(decodedLog)

                #     # The decoded log is written in JSON format to an output file
                #     with open('output/events.json', 'a') as events:
                #         json.dump(decodedLog, events, indent=4)
                #         # json.dump(decodedLog, events)
                #         events.write('\n')

                # else:
                #     print('\n** Not matched decoder. Log skipped. **')

            except:
                print('\nInvalid log format.')
                continue

if __name__ == '__main__':
    main()