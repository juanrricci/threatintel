import glob
import yaml

def fetchDecoders():
    decoderFiles = glob.glob('decoders/*.yml')
    formatsOfDecoders = {"json": [], "plaintext": [], "xml": []}
    for decoderFile in decoderFiles:
        with open(decoderFile) as decoderFileOpened: 
            decoderDict = yaml.load(decoderFileOpened, Loader=yaml.FullLoader)
            formatsOfDecoders[decoderDict['format']].append({'prematch': decoderDict['prematch'], 'filename': decoderFile})

    return formatsOfDecoders