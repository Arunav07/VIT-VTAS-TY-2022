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
