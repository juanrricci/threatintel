from benedict import benedict
from pprint import pprint

def checkFields(benedictedLog, decoderFields):
    for field in decoderFields:
        print('\n-- Checking field', field)
        if not field in benedictedLog:
            print('\n--- Field', field, 'is invalid. Decoder invalid too.')
            return False
        else:
            print('\n--- Field', field, 'is valid. Checking the following one...')
    print('\n- All fields are valid. Matched decoder.')
    return True

def checkMatchedDecoders(rawLog, matchedDecoders):
    benedictedLog = benedict(rawLog)
    for decoder in matchedDecoders:
        print('\n* Checking decoder', decoder['filename'])
        if checkFields(benedictedLog, decoder['prematch']['has_field']):
            print('\nMatched decoder:', decoder['filename'])
            return decoder['filename']
    print('\n* None of listed decoders have matched.')
    return False

def prematch(predecodedLog, decodersByFormat):
    matchedDecoders = decodersByFormat[predecodedLog['log']['type']]
    print('\nMatched JSON Decoders:') 
    pprint(matchedDecoders)
    return checkMatchedDecoders(predecodedLog['log']['raw'], decodersByFormat[predecodedLog['log']['type']])
