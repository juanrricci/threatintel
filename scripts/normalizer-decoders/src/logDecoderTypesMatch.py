from benedict import benedict

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
