import re

def formatByType(type):
    format = {
        '1': 'json',
        '4': 'undefined'
    }

    return format.get(type, 'Invalid log type')

def predecode(log):
    m = re.search('^(?P<type>\d):\[(?P<someid>\d+)\] \((?P<agentname>[\w-]+)\) (?P<ip>\d+\.\d+\.\d+\.\d+):(?P<port>\d+):(?P<path>[\/\w-]+):(?P<rawlog>.+)', log)
    print('M:', m.groups())
    
    return formatByType(m.group('type'))