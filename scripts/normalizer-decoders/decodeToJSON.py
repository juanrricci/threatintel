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

            try:
                # Read logs are predecoded for extracting context information.
                predecodedLog = predecode(log)
                print('\nVuelve del predecoder:')
                pprint(predecodedLog)

                # Predecoded logs are prematched for finding the right decoder.
                chosenDecoderFilename = prematch(predecodedLog, decodersByFormat)
                print('\nPrematch result:', chosenDecoderFilename)

                fullDecodedLog = predecodedLog.copy()

                # decodedEvent = decode(predecodedLog, chosenDecoderFilename)
                # decodedlog = fullDecodedLog + decodedEvent
                # Once the right decoder is found, the log information is decoded
                # and stored in normalized fields.
                fullDecodedLog = decode(predecodedLog, chosenDecoderFilename)
                pprint(fullDecodedLog)

                # The decoded log is written in JSON format to an output file
                with open('output/normalized_decodification4.json', 'w') as normalizedDecodification:
                    json.dump(fullDecodedLog, normalizedDecodification, indent=4)

            except:
                print('\nINVALID LOG FORMAT')
                continue

if __name__ == '__main__':
    main()