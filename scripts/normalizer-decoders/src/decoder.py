from benedict import benedict

def checkPrematchConditions(rawLog, matchedDecoders):
    benedictedLog = benedict(rawLog)
    for decoder in matchedDecoders:
        for field in decoder['prematch']['has_field']:
            if not field in benedictedLog:
                print('\nPrematch field', field, 'not found.')
                break
                # Finish the nested loop for continuing checking the following decoder fields
            else: print('Prematch field', field, 'found. OK.')
        # If all fields of the decoder match, this is the proper decoder
        return True
    # If all decoders fail, return False
    return False

def decode(predecodedLog, decodersByFormat):
    matchedDecoders = decodersByFormat[predecodedLog['log']['type']]
    print('\nMatched JSON Decoders:', matchedDecoders)
    print('\nPrematch result:', checkPrematchConditions(predecodedLog['log']['raw'], decodersByFormat[predecodedLog['log']['type']]))
    # applyMatchedDecoders(matchedDecoders, predecodedLog.get('log').get('raw'))

    # return predecodedLog