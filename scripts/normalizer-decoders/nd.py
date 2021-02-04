import json
import yaml

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def windowsLogDecode(windowsLog):
    with open('000-Windows.yml') as windowsDecoderFile:
        windowsDecoders = yaml.load(windowsDecoderFile, Loader=yaml.FullLoader)
        print(windowsDecoders)
        

def main():
    with open('logs.log') as logs:
        for log in logs:
            if validateJSON(log):
                # Assume this is a Windows log
                print('Valid Windows log.')
                windowsLogDecode(log)
            else:
                # Assume this is a syslog log
                print('Valid Syslog log.')

if __name__ == "__main__":
    main()