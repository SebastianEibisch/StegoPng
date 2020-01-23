import sys
import zlib

def ihdrData(targetFile):
    self.read(targetFile, 8) # größe
    bitDepth = int( self.read(targetFile, 1).hex(), 16)
    print("->Bit depth:", bitDepth)
    colorType = int( self.read(targetFile, 1).hex(), 16)
    print("->Color Type:", colorType)
    compression = int( self.read(targetFile, 1).hex(), 16)
    print("->Compression:", compression)
    filterMethod = int( self.read(targetFile, 1).hex(), 16)
    print("->Filter method:", filterMethod)
    interlace = int( self.read(targetFile, 1).hex(), 16)
    print("->Interlace:", interlace)

def decompress(content : bytes):
    content = zlib.decompress(content, 15)
    with open("idat_result.txt", "wb") as resultFile:
        resultFile.write(content)

def analyze(file):
    with open(file, "rb") as targetFile:
        header = self.read(targetFile, 8).hex()
        print("Header:", header)

        while True:
            chunkSize = int( self.read(targetFile, 4).hex(), 16 )
            print("Chunk Size:", chunkSize)
            chunkType = self.read(targetFile, 4).decode('ascii')
            print("Chunk Type:", chunkType)
              
            if chunkType == "tEXt" and chunkSize > 0:
                content = targetFile.read(chunkSize)
                print(content)
            elif chunkType == "IHDR":
                ihdrData(targetFile)
            elif chunkType == "IDAT":
                zlibCompression = self.read(targetFile, 1)
                print("->zLib compression bits:", bin( int( zlibCompression.hex(), 16 ) ).replace("0b", ""), "hex=", zlibCompression.hex())
                #print("-->bit 0-3 zLib compression-level | bit 4-7 ")
                additionalFlag = self.read(targetFile, 1)
                print("->flags bits:", bin( int( additionalFlag.hex(), 16) ).replace("0b", ""), "hex=", additionalFlag.hex())
                content = targetFile.read(chunkSize-6)
                checkValue = self.read(targetFile, 4)
                
                decompress(zlibCompression + additionalFlag + content + checkValue)
                print("->checkValue (?):", int(checkValue.hex(), 16))
            else:
                targetFile.read(chunkSize)

            crcSum = self.read(targetFile, 4).hex()
            print("CRC:", crcSum)

            if chunkType == "IEND":
                print("EOF")
                break

if __name__ == '__main__':
    analyze(sys.argv[1])



'''
idat
-> 1byte compression/flags
-> 1byte zusatzflags
-> nbyte komprimierte bilddaten
-> 4byte check

--> bildaten -> dekomprimieren -> "defiltern" -> fertig

zlib compression byte = hex 78 (1111000) -> zlib decompression mit 32k sliding window

zlib header
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

