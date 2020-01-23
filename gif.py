import math

IMAGE_SEPERATOR = 0x2C

file = open("sample.gif", "rb")

#header
print('Signature:', file.read(3).decode('ascii'))
print('Version:', file.read(3).decode('ascii'))

#logical screen descriptor
print('Width: (?)', int(file.read(2).hex(),16) )
print('Heigth: (?)', int(file.read(2).hex(),16) )

packedFields = bin( int(file.read(1).hex(),16) ).replace("0b", "")
print("PackedFields Bits:", packedFields)
print("==> Global Color Table Flag:", packedFields[0], "(1=yes, 0=no)")
print("==> Color Resolution Bits:", packedFields[1:4])
print("==> Sort Flag:", packedFields[4], "(1=ordered, 0=not ordered)")
colorTableValue = int(packedFields[5:], 2)
colorTableSize  = int(math.pow(2, colorTableValue))
print("==> Global Color Table Size:", colorTableSize, "bytes")
print("Background-Color-Index", int( file.read(1).hex(),16 ))
print("Pixel Aspect Ratio", int( file.read(1).hex(),16 ))

#color table?
print("Color-Table:")
for i in range(colorTableSize):
    #red, green, blue?
    rest = i % 3
    if rest == 0:
        color = "red"
    elif rest == 1:
        color = "green"
    elif rest == 2:
        color = "blue"
    
    print("==> "+str(i)+":", int(file.read(1).hex(),16), "("+color+")")

while True:
    byte = file.read(1) 
    
    if byte.hex() == IMAGE_SEPERATOR:
        print(byte.hex())
        break