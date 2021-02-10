from benedict import benedict

def existFields(jsonLog, prematchFields):
    for prematchField in prematchFields:
        benedictedLog = benedict(jsonLog)
        if not prematchField in benedictedLog:
            print('Prematch field', prematchField, 'not found.')
            return False
        else: print('Prematch field', prematchField, 'found. OK.')
    return True
