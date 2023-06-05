import os
import binascii
import hashlib
import time


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

print("Now finding duplicates")

for j in range(1, chunk):
     with open(filePath + (str(j)), "rb") as f:
        data = f.read()
        with open("Hashes/MD5/hashFile_"+(str(j))+".txt", "wt+") as hash_file_MD5:
            hash_file_MD5.write(hashlib.md5(data.encode('utf-8')).hexdigest())
        with open("Hashes/SHA1/hashFile_" + (str(j)), "wt+") as hash_file_SHA1:
            hash_file_SHA1.write(hashlib.sha1(data.encode('utf-8')).hexdigest())
        with open("Hashes/SHA256/hashFile_" + (str(j)), "wt+") as hash_file_SHA256:
            hash_file_SHA256.write(hashlib.sha256(data.encode('utf-8')).hexdigest())

dedupHashTable_MD5 = {}
for j in range(1, chunk):
    with open("Hashes/MD5/hashFile_"+(str(j))+".txt", "r") as f:
        data = f.read()
        if data in dedupHashTable_MD5:
            dedupHashTable_MD5[data].append(j)
        else:
            dedupHashTable_MD5[data] = [j]

dedupHashTable_SHA1 = {}
for j in range(1, chunk):
    with open("Hashes/SHA1/hashFile_"+(str(j)), "r") as f:
        data = f.read()
        if data in dedupHashTable_SHA1:
            dedupHashTable_SHA1[data].append(j)
        else:
            dedupHashTable_SHA1[data] = [j]

dedupHashTable_SHA256 = {}
for j in range(1, chunk):
    with open("Hashes/SHA256/hashFile_"+(str(j)), "r") as f:
        data = f.read()
        if data in dedupHashTable_SHA256:
            dedupHashTable_SHA256[data].append(j)
        else:
            dedupHashTable_SHA256[data] = [j]

print("Duplicates found using SHA256: ")
for k in range(len(dedupHashTable_SHA256)):
    if(len(dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]])>1):
        # writing duplicates to text
        locations = list(map(str, dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]]))
        with open("Duplicates.txt", "at+") as f:
            f.write(open("Chunks/chunkFile_"+(str(dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]][0]))+".txt", "r").read()[:-2]+","+("--").join(locations)+"\n")
        f.close()
