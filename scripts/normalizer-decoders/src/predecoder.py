import re

def formatByType(type):
    format = {
        '1': 'json',
        '4': 'undefined'
    }

    return format.get(type, 'Invalid log type')

def predecode(log):
    m = re.search('^(?P<type>\d):', log)
    
    return formatByType(m.group('type'))