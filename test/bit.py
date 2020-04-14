'''
original = b"h"

binary = bin(original[0]).replace("0b","")

print(binary)


length = 3 # das sollte parametrierbar sein

print(binary[ len(binary)-length ])







0 1 2 3 4  
h a l l o



original = "234567"

string = ["hallo", "alter"]
length = 3 # das sollte parametrierbar sein

manipulated = ""
for index in range(length):
    manipulated += "X"

print( string[:len(string)-length] )
print( string[:len(string)-length] + manipulated )

'''


class Manipulator:
    def __init__(self, length : int):
        self._sizePerByte = length

    def hide(self, content : bytes, messageToHide : bytes) -> bytes:
        secretBitStream = self._toBitStream(messageToHide)
        print("debug", messageToHide)
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
            print("debug", element)
            stream += self._toBin(element)
        print("debug", stream)
        return stream


    def _toBin(self, value) -> str:
        return format(value, "#010b").replace('0b', '')

    def _toInt(self, value) -> int:
        return int(value,2)




content = b'hallo du da'
secret  = b'ab'
secretBits = ''
test = b'123456789'
print(test[2:-4])
exit()
print("---- secret ----")
for index, element in enumerate(secret):
    secretBits += format(12, '#010b').replace('0b', '')
print(secretBits)

print("---- original ----")
for index, element in enumerate(content):
    print(format(content[index], '#010b'))

##################################################

mani = Manipulator(2)
manipulatedBytes = mani.hide(content, secret)
'''
manipulatedBytes = []
secretBitsPointer = 0
length = 2
for byte in content:
    if secretBitsPointer+length > len(secretBits):
        manipulatedBytes.append(byte)
        continue

    bits = format(byte, '#010b')
    bits = bits[:len(bits)-length] + secretBits[secretBitsPointer:secretBitsPointer+length]
    manipulatedBytes.append(int(bits,2))
    secretBitsPointer += length
    
'''
#################################################

print("---- manipuliert ----")
for index, element in enumerate(manipulatedBytes):
    print(format(manipulatedBytes[index], '#010b'))

print( str(bytes(manipulatedBytes)) )

