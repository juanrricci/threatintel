import re


def wcsParse():
    wcsList = set()
    with open('wcs-fields.list') as wcsFields:
        for wcsField in wcsFields:
            wcsRootField = re.split('\.|\\n', wcsField, maxsplit=1)
            wcsList.add(wcsRootField[0])
    return sorted(wcsList)
