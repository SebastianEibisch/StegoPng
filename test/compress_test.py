import zlib

class Test:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.bytePointer = 0

    def copy(self):
        (prefix, idatChunk) = self._seek_idat()
        suffixBytes = self._seek_suffix()
        print("Prefix:", len(prefix), "bytes")
        print("IDAT:", len(idatChunk), "bytes")
        print("Suffix", len(suffixBytes), "bytes")

        uncompressedIdat = zlib.decompress(idatChunk, 15)
        recompressedIdat = zlib.compress(uncompressedIdat, 8)

        self.target.write(prefix + recompressedIdat + suffixBytes)
        self.target.close()
        self.source.close()

    def _seek_idat(self):
        self._read_bytes_hex(8) #header
        chunkType = ""
        chunkSize = ""
        chunkContent = ""
        chunkCRC = ""
        bytes_read = b""
        idatFound = False
        while idatFound == False:
            chunkSize = self._read_bytes(4)
            chunkType = self._read_bytes(4)

            bytes_read = chunkSize + chunkType
            
            if chunkType.decode("ascii") == 'IDAT':
                print("IDAT gefunden!")
                chunkContent = self._read_bytes( int( chunkSize.hex(), 16 ) )
                break

            chunkContent = self._read_bytes( int( chunkSize.hex(), 16 ) )
            chunkCRC = self._read_bytes(4)
            bytes_read = chunkContent + chunkCRC
        
        return bytes_read, chunkContent

    def _seek_suffix(self):
        chunkType = b""
        chunkSize = b""
        chunkContent = b""
        chunkCRC = b""
        iendFound = False
        bytes_read = b""
        while iendFound == False:
            chunkSize = self._read_bytes(4)
            chunkType = self._read_bytes(4)
            if chunkType.decode("ascii") != "IEND":
                chunkContent = self._read_bytes( int( chunkSize.hex(), 16 ) )
            else:
                iendFound = True
            chunkCRC = self._read_bytes(4)

        bytes_read = chunkSize + chunkType + chunkContent + chunkCRC

        return bytes_read

    def _read_bytes(self, length) -> bytes:
        self.bytePointer += length
        return self.source.read(length)

    def _read_bytes_hex(self, length):
        return self._read_bytes(length).hex()

    def _read_bytes_ascii(self, length):
        return self._read_bytes(length).decode("ascii")

    def _read_bytes_int(self, length):
        return int( self._read_bytes_hex(length), 16 )

if __name__ == "__main__":
    source = open("sample2.png", "rb")
    target = open("target.png", "wb")
    Test(source, target).copy()