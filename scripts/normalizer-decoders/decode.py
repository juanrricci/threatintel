import json

from src.predecoder import predecode
from src.decoder import decode
from src.validateJSON import isJSON
from src.decoderGather import parseAllDecoderFiles
from src.logDecoderTypesMatch import existFields
from src.normalizer import createJsonOutput


def main():
    decodersByFormat = parseAllDecoderFiles()
    print('Format of decoders:', decodersByFormat)

    # - Iterate over logs.
    # -- Iterate over decoders.
    # --- Check if decoder has 'has_field' prematch and log is JSON.
    # ---- If True: check if field exists. If False: skip decoder.
    # ----- If True: decode.
    # --- Check if decoder has 'regex' prematch and log is not JSON.
    # ---- If True: check if regex matches. If False: skip decode.
    # ----- If True: decode.

    with open('logs.log') as logs:
        for log in logs:
            # parseo de la linea de log, tiene que sacar id del tipo de log y datos del agente, y el log propiamente
            # case 1:
            #       es un JSON -> linea 95
            #       ya sabe que es un JSON, salta directamente à la decodificacion
            # case 4:
            #       es un JSON? -> valida
            try:
            # if True:
                predecodedLog = predecode(log)
                print('\nVuelve del predecoder:', predecodedLog)

                decode(predecodedLog, decodersByFormat)
            #     logIsJSON = isJSON(log)
            #     jsonLog = json.loads(log) if logIsJSON else False
            #     for prematchToDecoderFilename in prematchToDecoderFilenameList:
            #         prematchType = list(prematchToDecoderFilename['prematch'].keys())[0]
            #         decoderFilename = prematchToDecoderFilename['filename']
            #         print(decoderFilename)
            #         # decoderFilename = 
            #         if prematchType == 'has_field' and logIsJSON:
            #             print('HAS FIELD and IS JSON')
            #             # print('Do fields exist?',existFields(jsonLog, prematchToDecoderFilename['prematch']['has_field']))
            #             if existFields(jsonLog, prematchToDecoderFilename['prematch']['has_field']):
            #                 createJsonOutput(jsonLog, decoderFilename)
            #         elif prematchType == 'regex' and not logIsJSON:
            #             print('REGEX and IS NOT JSON')
            #         else:
            #             print('Exception:')
            #             print('Prematch Type:', prematchType)
            #             print('Log is JSON:', logIsJSON)
            except:
                print('Invalid log format')
                continue

if __name__ == '__main__':
    main()