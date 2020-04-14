import zlib
import logging

IMAGE_WIDTH = "pictureWidth"
PAYLOAD = "payload"
DEBUG = "debug"
IDAT_CHUNK = "idatChunk"
DEBUG_PREFIX = "[IdatInjector]"

logging.basicConfig(filename='log/logfile', level=logging.DEBUG, format='%(asctime)s %(message)s')

class IdatInjector:

    def __init__(self):
        pass

    def injectPayload(self, **args : dict):
        (scanlineSize, payload, idat) = self.__checkArgs(args)
        
        logging.debug('injecting payload ...')
        logging.debug('size of recieved idat chunk %s bytes' % len(idat))
        logging.debug('decompression level detected %s' % idat[:2].hex())
        idat = zlib.decompress(idat[2:-4], -15)

        pass

    def __checkArgs(self, args : dict) -> (int, bytes, bytes):
        requiredArgs = [IMAGE_WIDTH, PAYLOAD, IDAT_CHUNK]
        logging.debug('idat injector arguments ...')
        for key in requiredArgs:
            if args.get(key) is None:
                print('required argument "%s" is missing!' % key)
                exit()
            
            if key is not PAYLOAD and key is not IDAT_CHUNK:
                logging.debug('%s : %s' % ( key, args.get(key) ))

        return args.get(IMAGE_WIDTH), args.get(PAYLOAD), args.get(IDAT_CHUNK)

if __name__ == '__main__':

    logging.debug('test')

    #fakeIdat = bytes([0,128,128,128,128,128,128,128,128,128, 0,128,128,128,128,128,128,128,128,128, 0,128,128,128,128,128,128,128,128,128])
   # IdatInjector().injectPayload(pictureWidth=10, payload=bytes([255,0,255,0]), debug=True, idatChunk=fakeIdat) 
     
        