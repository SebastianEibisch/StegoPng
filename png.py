import zlib

class PngStego:
    def __init__(self, file):
        self._bytePointer = 0
        self._sourceFile = file
    
    def _read(self, length : int) -> bytes:
        self._bytePointer += length
        return self._sourceFile.read(length)

    def _ihdrData(self):
        width = int( self._read(4).hex(), 16)
        print("->Width:", width)
        height = int( self._read(4).hex(), 16)
        print("->Height:", height)
        bitDepth = int( self._read(1).hex(), 16)
        print("->Bit depth:", bitDepth)
        colorType = int( self._read(1).hex(), 16)
        print("->Color Type:", colorType)
        compression = int( self._read(1).hex(), 16)
        print("->Compression:", compression)
        filterMethod = int( self._read(1).hex(), 16)
        print("->Filter method:", filterMethod)
        interlace = int( self._read(1).hex(), 16)
        print("->Interlace:", interlace)

    def analyse(self):
        header = self._read(8).hex()
        print("Header:", header)

        while True:
            print("-------------")
            chunkSize = int( self._read(4).hex(), 16 )
            print("Chunk Size:", chunkSize)
            chunkType = self._read(4).decode('ascii')
            print("Chunk Type:", chunkType)
            
            if chunkType == "tEXt" and chunkSize > 0:
                content = self._read(chunkSize)
                print(content)
            elif chunkType == "IHDR":
                self._ihdrData()
            elif chunkType == "IDAT":
                zlibCompression = self._read(1)
                print("->zLib compression bits:", bin( int( zlibCompression.hex(), 16 ) ).replace("0b", ""), "hex=", zlibCompression.hex())
                additionalFlag = self._read(1)
                print("->flags bits:", bin( int( additionalFlag.hex(), 16) ).replace("0b", ""), "hex=", additionalFlag.hex())
                content = self._read(chunkSize-6)
                checkValue = self._read(4)
                print("->checkValue (?):", int(checkValue.hex(), 16))
            else:
                self._read(chunkSize)

            crcSum = self._read(4).hex()
            print("CRC:", crcSum)

            if chunkType == "IEND":
                print("EOF")
                break

    def manipulateAndCopy(self, targetFile):
        targetFile.write(self._read(8))
        while True:
            chunkSizeBytes = self._read(4)
            chunkTypeBytes = self._read(4)

            if chunkTypeBytes.decode('ascii') == "IDAT":
                print('IDAT found!')
                zlibCompression = self._read(1)
                additionalFlag = self._read(1)
                content = self._read(int(chunkSizeBytes.hex(), 16)-6)

                maniContent = self._manipulateIdat(content)
                print("-> injecting payload!")

                chunkSizeBytes = int(chunkSizeBytes.hex(),16)
                chunkSizeBytes += len(maniContent) - (len(content)+6)
                targetFile.write( chunkSizeBytes.to_bytes(4,"big") )
                targetFile.write( chunkTypeBytes )
                targetFile.write( maniContent )

                checkValue = self._read(4)
            else:
                print("Chunk", chunkTypeBytes.decode('ascii'), "read...")
                targetFile.write(chunkSizeBytes + chunkTypeBytes)
                targetFile.write( self._read( int(chunkSizeBytes.hex(), 16) ) )

            targetFile.write(self._read(4)) #CRC

            if chunkTypeBytes.decode('ascii') == "IEND":
                break 

    def _manipulateIdat(self, content):
        uncompressedContent = zlib.decompress(content, -15)
        manipulatedContent = self._manipulateByte(uncompressedContent)
        compressedContent = zlib.compress(manipulatedContent, 5)
        return compressedContent
    
    def _manipulateByte(self, content):
        newBytes = []
        for index, byte in enumerate(content):
            if index == 1:
                newBytes.append(255)
            else:
                newBytes.append(byte)

        return bytes(newBytes)

    def extractIdat(self, sourceFile, destination):
        sourceFile.read(8)
        while True:
            chunkSizeBytes = sourceFile.read(4)
            chunkTypeBytes = sourceFile.read(4)

            if chunkTypeBytes.decode('ascii') == "IDAT":
                print('IDAT found!')
                zlibCompression = sourceFile.read(1)
                additionalFlag = sourceFile.read(1)

                content = sourceFile.read(int(chunkSizeBytes.hex(), 16)-6)
                print("-> decompressing idat chunk")
                destinationFile = open(destination, "wb")
                destinationFile.write(zlib.decompress(content, -15))
                destinationFile.close()
                print("-> result written to", destination)
                break
            else:
                print("Chunk", chunkTypeBytes.decode('ascii'), "read...")
                sourceFile.read( int(chunkSizeBytes.hex(), 16) )
            
            sourceFile.read(4) #CRC

            if chunkTypeBytes.decode('ascii') == "IEND":
                break 

if __name__ == '__main__':
    filename = "sample2.png"
    target = "manipulated.png"

    idat_orig_result = "idat_original.chunk"
    idat_mani_result = "idat_manipulated.chunk"
    
    
    
    sampleFile = open(filename, "rb")
    stego = PngStego(sampleFile)
    stego.analyse()
    sampleFile.seek(0)
    stego.extractIdat(sampleFile, idat_orig_result)
    
    
    
    '''
    with open(filename, "rb") as pngimage, open(target, "ab") as targetFile:
        stego = PngStego(pngimage)
        stego.manipulateAndCopy(targetFile)

    with open(filename, "rb") as origFile, open(target, "rb") as maniFile:
        stego = PngStego(filename)
        stego.extractIdat(origFile, idat_orig_result)
        stego.extractIdat(maniFile, idat_mani_result)
    '''
'''
Color Type
-----------------------------
Greyscale               0
Truecolour              2
Indexed-colour          3
Greyscale with alpha    4
Truecolour with alpha   6

zlib header
-----------------------------
Level | ZLIB  | GZIP 
  1   | 78 01 | 1F 8B 
  2   | 78 5E | 1F 8B 
  3   | 78 5E | 1F 8B 
  4   | 78 5E | 1F 8B 
  5   | 78 5E | 1F 8B 
  6   | 78 9C | 1F 8B 
  7   | 78 DA | 1F 8B 
  8   | 78 DA | 1F 8B 
  9   | 78 DA | 1F 8B 

    '''
