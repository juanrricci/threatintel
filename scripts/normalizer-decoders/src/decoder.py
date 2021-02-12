from benedict import benedict

def checkFields(benedictedLog, decoderFields):
    for field in decoderFields:
        print('\nChecking field', field)
        if not field in benedictedLog:
            print('\nField', field, 'is invalid. Decoder invalid too.')
            return False
        else:
            print('\nField', field, 'is valid. Checking the following one...')
    print('\nAll fields are valid. Matched decoder.')
    return True

def checkMatchedDecoders(rawLog, matchedDecoders):
    benedictedLog = benedict(rawLog)
    for decoder in matchedDecoders:
        print('\nChecking decoder', decoder['filename'])
        if checkFields(benedictedLog, decoder['prematch']['has_field']):
            print('\nMatched decoder:', decoder['filename'])
            return decoder['filename']
    print('\nNone of listed decoders have matched.')
    return False

def decode(predecodedLog, decodersByFormat):
    matchedDecoders = decodersByFormat[predecodedLog['log']['type']]
    print('\nMatched JSON Decoders:', matchedDecoders)
    print('\nPrematch result:', checkMatchedDecoders(predecodedLog['log']['raw'], decodersByFormat[predecodedLog['log']['type']]))
