import re
import json

def findLogType(rawLog):
    try:
        json.loads(rawLog)
    except ValueError as err:
        return 'plaintext'
    return 'json'


def formatByType(logType, rawLog):
    format = {
        '1': 'json',
        '4': findLogType(rawLog)
    }

    return format.get(logType, 'Invalid log type')

def predecode(log):
    try:
    # if True:
        m = re.search('^(?P<log_type>\d):\[(?P<agent_id>\d+)\] \((?P<agent_name>[\w-]+)\) (?P<agent_ip>\d+\.\d+\.\d+\.\d+):(?P<agent_port>\d+):(?P<agent_location>[\/\w-]+):(?P<raw_log>.+)', log)
        print('\nGROUPS:', m.groups())
        print('\nlog_type:', m.group('log_type'))
        print('\nagent_id:', m.group('agent_id'))
        predecoding = {
            'agent': {
                'id': m.group('agent_id'),
                'name': m.group('agent_name'),
                'ip': m.group('agent_ip'),
                'location': m.group('agent_location')
            },
            'log': {
                'type': formatByType(m.group('log_type'), m.group('raw_log')),
                'raw': m.group('raw_log')
            }
        }
    except:
        return 'Invalid log format'

    return predecoding
