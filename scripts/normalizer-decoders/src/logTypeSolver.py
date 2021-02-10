import re

def getLogType(log):
    m = re.search('^(?P<type>\d):', log)
    return m.group('type')