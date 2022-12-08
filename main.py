import os
import binascii
import dedupe

file = open("text.txt", "r")
binaryFile = open("binary.txt", "wt+")
# Path: text.txt
i=0 
with open("text.txt", "r") as f:
    for line in f:
        i+=1
        # print("{} : {}".format(line.strip(),int(str( bin(int(binascii.hexlify(line.strip().encode('utf8')), 16)))[2:])))
        binaryFile.write("{}\n".format(int(str(bin(int(binascii.hexlify(line.strip().encode('utf8')), 16)))[2:])))
i=1
binaryFile.close()
binaryFile = open("binary.txt", "r")

print("Now splitting binary file")
chunk_size = 64
with open ("binary.txt", "r") as myfile:
    chunk = myfile.read(chunk_size)
    while (chunk != ""):
        with open("Chunks/chunkFile_"+(str(i)), "wt+") as chunk_file:
            if('\n' in chunk):
                chunk = chunk.split("\n")
                chunk_file.write(chunk[0])
                chunk_file.write(chunk[1])
            else:
                chunk=""
        i+=1
        chunk = myfile.read(chunk_size)


# Using Hashing algorithms to find duplicates
import hashlib

print("Now finding duplicates")
for j in range(1, i):
    with open("Chunks/chunkFile_"+(str(j)), "r") as f:
        data = f.read()
        with open("Hashes/MDA5/hashFile_"+(str(j)), "wt+") as hash_file_MDA5:
            hash_file_MDA5.write(hashlib.md5(data.encode('utf-8')).hexdigest())
        with open("Hashes/SHA1/hashFile_"+(str(j)), "wt+") as hash_file_SHA1:
            hash_file_SHA1.write(hashlib.sha1(data.encode('utf-8')).hexdigest())


# Using Dedupe to find duplicates in MDA5 Hashes
# deduper = dedupe.Dedupe(fields)
# for j in range(1, i-1):
#     with open("Hashes/MDA5/hashFile_"+(str(j)), "r") as f:
#         data = f.read()
#         deduper.sample(data)


# Using Dedupe to find duplicates in SHA1 Hashes


