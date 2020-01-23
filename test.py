import sys
import zlib
class Test:
    def __init__(self):
        self.bytePointer = 0
    
    def read(self, file, length : int) -> bytes:
        self.bytePointer += length
        return file.read(length)

    def ihdrData(self, targetFile):
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

    def decompress(self, content : bytes):
        content = zlib.decompress(content, -15)
        with open("idat_result.txt", "wb") as resultFile:
            resultFile.write(content)

    def manipulate(self, compression : bytes, flags : bytes, content : bytes, check : bytes, file):
        content = zlib.decompress(compression + flags + content + check, 15)
        print(len(content))
        # n bytes manipulieren
        mutableBytes = []
        for i in range(0, len(content), 2):
            mutableBytes.append(255)

        print(len(bytes(mutableBytes).hex()))
        manipulatedBytes = zlib.compress(bytes(mutableBytes), 8)
        print(len(bytes(manipulatedBytes).hex()))

        # seek auf bytePointer - n - 4
        
        # write n manipulierte bytes
        # dummy read 4






    def manipulateByte(self, content):
        newBytes = []
        for index, byte in enumerate(content):
            if index == 1:
                newBytes.append(255)
            else:
                newBytes.append(byte)
        return bytes(newBytes)

    def uncompressTest(self, content):
        print("compressed size:", len(content))
        uncompressedContent = zlib.decompress(content, -15)
        print("uncompressed size:", len(uncompressedContent))
        uncompressedContent = self.manipulateByte(uncompressedContent)
        compressedContent = zlib.compress(uncompressedContent, 5)
        print("compressed size:", len(compressedContent))
        open("uncompressed", "wb").write(uncompressedContent)

        zlibCompression = compressedContent[0]
        print("==>zLib compression bits:", bin(zlibCompression), "hex=", hex(zlibCompression))
        additionalFlag = compressedContent[1]
        print("==>flags bits:", bin( additionalFlag ), "hex=", hex(additionalFlag))
        print("==>checkValue (?):", int( compressedContent[-4:].hex(), 16) )









    def uncompressTest2(self, content):
        print("compressed size:", len(content))
        uncompressedContent = zlib.decompress(content, 15)
        print("uncompressed size:", len(uncompressedContent))
        compressedContent = zlib.compress(uncompressedContent, 8)
        print("compressed size:", len(compressedContent))

    def analyze(self, file):
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
                    self.ihdrData(targetFile)
                elif chunkType == "IDAT":
                    zlibCompression = self.read(targetFile, 1)
                    print("->zLib compression bits:", bin( int( zlibCompression.hex(), 16 ) ).replace("0b", ""), "hex=", zlibCompression.hex())
                    additionalFlag = self.read(targetFile, 1)
                    print("->flags bits:", bin( int( additionalFlag.hex(), 16) ).replace("0b", ""), "hex=", additionalFlag.hex())
                    content = self.read(targetFile, chunkSize-6)
                    checkValue = self.read(targetFile, 4)
                    
                    #self.decompress(content)
                    #self.manipulate(zlibCompression, additionalFlag, content, checkValue, file)
                    self.uncompressTest(content)
                    #print("-----")
                    #self.uncompressTest2(zlibCompression + additionalFlag + content + checkValue)
                    print("->checkValue (?):", int(checkValue.hex(), 16))
                else:
                    targetFile.read(chunkSize)

                crcSum = self.read(targetFile, 4).hex()
                print("CRC:", crcSum)

                if chunkType == "IEND":
                    print("EOF")
                    break

if __name__ == '__main__':
    
    #Test().analyze(sys.argv[1])
    Test().analyze("sample2.png")




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

