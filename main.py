import os
import binascii
import hashlib


chunkSize = 64  # bytes
filePath = "text.txt"

# File to open and break apart
fileR = open(filePath, "rb")

chunk = 0

byte = fileR.read(chunkSize)
print("Now splitting binary file")
while byte:
    # Open a temporary file and write a chunk of bytes
    fileN = filePath + str(chunk)
    fileT = open("fileN", "wb")
    fileT.write(byte)
    fileT.close()

    # Read next 64 bytes
    byte = fileR.read(chunkSize)

    chunk += 1
