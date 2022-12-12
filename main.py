import binascii

file = open("text.txt", "r")
binaryFile = open("binary.txt", "wt+")
textFile = open("textWrite.txt", "wt+")
# Path: text.txt
i=0 
with open("text.txt", "r", encoding='utf-8') as f:
    for line in f:
        if(line=="\n"):
            pass
        else:
            binaryFile.write("{}\n".format(int(str(bin(int(binascii.hexlify(line.strip().encode('utf8')), 16)))[2:])))
            textFile.write("{}\n".format(line.strip()))
i=1
binaryFile.close()
binaryFile = open("binary.txt", "r")

print("Now splitting binary file")
chunk_size = 10240
with open ("binary.txt", "r") as myfile:
    chunk = myfile.read(chunk_size)
    while (chunk != ""):
        with open("Chunks/chunkFile_"+(str(i)), "wt+") as chunk_file:
            chunk_file.write(chunk)
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

dedupHashTable_MDA5 = {}
for j in range(1, i):
    with open("Hashes/MDA5/hashFile_"+(str(j)), "r") as f:
        data = f.read()
        if data in dedupHashTable_MDA5:
            dedupHashTable_MDA5[data].append(j)
        else:
            dedupHashTable_MDA5[data] = [j]

dedupHashTable_SHA1 = {}
for j in range(1, i):
    with open("Hashes/SHA1/hashFile_"+(str(j)), "r") as f:
        data = f.read()
        if data in dedupHashTable_SHA1:
            dedupHashTable_SHA1[data].append(j)
        else:
            dedupHashTable_SHA1[data] = [j]

print("Duplicates found using MDA5: ")
for k in range(len(dedupHashTable_MDA5)):
    if(len(dedupHashTable_MDA5[list(dedupHashTable_MDA5.keys())[k]])>1):
        print("Duplicate files are: ",k)
        print( list(dedupHashTable_MDA5.keys())[k], " : ", dedupHashTable_MDA5[list(dedupHashTable_MDA5.keys())[k]])
        print(open(textFile.name).read().splitlines()[dedupHashTable_MDA5[list(dedupHashTable_MDA5.keys())[k]][0]-1])
            