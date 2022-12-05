import os
import binascii

file = open("text.txt", "r")
binaryFile = open("binary.txt", "wt+")
# Path: text.txt
i=0
with open("text.txt", "r") as f:
    for line in f:
        i+=1
        print("{} : {}".format(line.strip(),int(str( bin(int(binascii.hexlify(line.strip().encode('utf8')), 16)))[2:])))
        binaryFile.write("{} : {}\n".format(line.strip(),int(str( bin(int(binascii.hexlify(line.strip().encode('utf8')), 16)))[2:])))
i=1
with open ("binary.txt", "r") as myfile:
    chunk = myfile.read(16)
    while chunk:
        with open("chunkFile_"+(str(i))) as chunk_file:
            chunk_file.write(chunk)
        i+=1
        chunk = myfile.read(16)