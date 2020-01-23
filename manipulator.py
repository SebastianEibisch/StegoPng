class Manipulator:
    def __init__(self, length : int):
        self._sizePerByte = length

    def hide(self, content : bytes, messageToHide : bytes) -> bytes:
        secretBitStream = self._toBitStream(messageToHide)
        
        manipulatedBytes = []
        bitPointer = 0
        for byte in content:
            if bitPointer + self._sizePerByte > len(secretBitStream):
                manipulatedBytes.append(byte)
                continue

            bits = format(byte, '#010b')
            bits = bits[:len(bits)-self._sizePerByte] + secretBitStream[bitPointer:bitPointer+self._sizePerByte]
            manipulatedBytes.append(int(bits,2))
            bitPointer += self._sizePerByte

        return bytes(manipulatedBytes)

    def show(self, content : bytes):
        pass

    def _toBitStream(self, value : bytes) -> str:
        stream = ''
        for element in value:
            stream += self._toBin(element)
        return stream

    def _toBin(self, value) -> str:
        return format(value, "#010b").replace('0b', '')

    def _toInt(self, value) -> int:
        return int(value,2)