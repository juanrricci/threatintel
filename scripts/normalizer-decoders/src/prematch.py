import re
from benedict import benedict
from pprint import pprint

def checkFields(benedictedLog, prematchFields):
    if 'condition' in prematchFields and prematchFields['condition'] == 'or':
        print('\n**** ESTO TIENE CONDICION OR ****')
        for field in prematchFields['has_field']:
            print('-- Checking field', field)
            if field in benedictedLog:
                print('--- Field', field, 'is valid. Matched decoder.')
                return True
            else:
                print('* Field', field, 'is invalid. Checking the following one...')
        print('* All fields are invalid. Decoder invalid too.')
        return False
    else:
        for field in prematchFields['has_field']:
            print('-- Checking field', field)
            if not field in benedictedLog:
                print('* Field', field, 'is invalid. Decoder invalid too.')
                return False
            else:
                print('--- Field', field, 'is valid. Checking the following one...')
        print('* All fields are valid. Matched decoder.')
        return True

def checkRegex(rawLog, prematchRegex):
    for regex in prematchRegex:
        print('-- Checking prematch regex', regex)
        if re.search(regex, rawLog):
            print('* Prematch regex', regex, 'is valid. Matched decoder.')
            return True
        else:
            print('--- Prematch regex', regex, 'is invalid. Checking the following one...')
    print('* All prematch regex are invalid. Decoder skipped.')
    return False

def checkJSONDecoders(rawLog, matchedDecoders):
    benedictedLog = benedict(rawLog)
    for decoder in matchedDecoders:
        print('\n* Checking decoder', decoder['filename'])
        if checkFields(benedictedLog, decoder['prematch']):
            print('\nMatched decoder:', decoder['filename'], 'by prematch fields.')
            return decoder['filename']
    print('\n* None of listed decoders have matched.')
    return False

def checkPlaintextDecoders(rawLog, matchedDecoders):
    for decoder in matchedDecoders:
        print('\n* Checking decoder', decoder['filename'])
        if checkRegex(rawLog, decoder['prematch']['regex']):
            print('\nMatched decoder:', decoder['filename'], 'by prematch regex.')
            return decoder['filename']
    print('\n* None of listed decoders have matched.')
    return False

def checkXMLDecoders(rawLog, matchedDecoders):
    print('XML decoders must be checked here.')

def prematch(predecodedLog, decodersByFormat):
    print('\nMatched Decoders:') 
    pprint(decodersByFormat[predecodedLog['log']['type']])
    formatsOfDecoders = {
        'json': checkJSONDecoders,
        'plaintext': checkPlaintextDecoders,
        'xml': checkXMLDecoders
    }

    return formatsOfDecoders.get(predecodedLog['log']['type'], 'Invalid log type')(predecodedLog['log']['raw'], decodersByFormat[predecodedLog['log']['type']])
    # return formatsOfDecoders.get(decodersByFormat[predecodedLog['log']['type']], 'Invalid log type')(predecodedLog['log']['raw'], decodersByFormat[predecodedLog['log']['type']])
    # return checkJSONDecoders(predecodedLog['log']['raw'], decodersByFormat[predecodedLog['log']['type']])
