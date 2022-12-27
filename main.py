import time

file = open("text.txt", "r")
textFile = open("textWrite.txt", "wt+")
# Path: text.txt
i=0 
with open("text.txt", "r", encoding='utf-8') as f:
    for line in f:
        if(line=="\n" or line=="\r"):
            pass
        else:
            textFile.write("{}\n".format(line.strip()))
i=1

filePath = "textWrite.txt"

print("Now splitting into chunks")
chunk_size = 64
with open (filePath, "rb") as myfile:
    chunk = myfile.read(chunk_size)
    while (chunk):
        fileN = "Chunks/chunkFile_"+(str(chunk))
        fileT = open(fileN, "wb")
        fileT.write(chunk)
        fileT.close()
        chunk = myfile.read(chunk_size)
        i+=1



# # Using Hashing algorithms to find duplicates
# import hashlib

# print("Now finding duplicates")
# time_MD5 = time.time()
# time_SHA1 = time.time()
# time_SHA256 = time.time()
# for j in range(1, i):
#     with open("Chunks/chunkFile_"+(str(j))+".txt", "r") as f:
#         data = f.read()
#         with open("Hashes/MD5/hashFile_"+(str(j))+".txt", "wt+") as hash_file_MD5:
#             hash_file_MD5.write(hashlib.md5(data.encode('utf-8')).hexdigest())
#         with open("Hashes/SHA1/hashFile_"+(str(j)), "wt+") as hash_file_SHA1:
#             hash_file_SHA1.write(hashlib.sha1(data.encode('utf-8')).hexdigest())
#         with open("Hashes/SHA256/hashFile_"+(str(j)), "wt+") as hash_file_SHA256:
#             hash_file_SHA256.write(hashlib.sha256(data.encode('utf-8')).hexdigest())

# dedupHashTable_MD5 = {}
# for j in range(1, i):
#     with open("Hashes/MD5/hashFile_"+(str(j))+".txt", "r") as f:
#         data = f.read()
#         if data in dedupHashTable_MD5:
#             dedupHashTable_MD5[data].append(j)
#         else:
#             dedupHashTable_MD5[data] = [j]

# dedupHashTable_SHA1 = {}
# for j in range(1, i):
#     with open("Hashes/SHA1/hashFile_"+(str(j)), "r") as f:
#         data = f.read()
#         if data in dedupHashTable_SHA1:
#             dedupHashTable_SHA1[data].append(j)
#         else:
#             dedupHashTable_SHA1[data] = [j]

# dedupHashTable_SHA256 = {}
# for j in range(1, i):
#     with open("Hashes/SHA256/hashFile_"+(str(j)), "r") as f:
#         data = f.read()
#         if data in dedupHashTable_SHA256:
#             dedupHashTable_SHA256[data].append(j)
#         else:
#             dedupHashTable_SHA256[data] = [j]
            
# print("Duplicates found using MD5: ")
# for k in range(len(dedupHashTable_MD5)):
#     if(len(dedupHashTable_MD5[list(dedupHashTable_MD5.keys())[k]])>1):
#         print( list(dedupHashTable_MD5.keys())[k], " : ", dedupHashTable_MD5[list(dedupHashTable_MD5.keys())[k]])
# end_MD5 = time.time()


# #converting 
# print("Duplicates found using SHA1: ")
# for k in range(len(dedupHashTable_SHA1)):
#     if(len(dedupHashTable_SHA1[list(dedupHashTable_SHA1.keys())[k]])>1):
#         locations = list(map(str, dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]]))
#         print( list(dedupHashTable_SHA1.keys())[k], " : ", dedupHashTable_SHA1[list(dedupHashTable_SHA1.keys())[k]])
# end_SHA1 = time.time()

# print("Duplicates found using SHA256: ")
# for k in range(len(dedupHashTable_SHA256)):
#     if(len(dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]])>1):
#         # writing duplicates to text
#         locations = list(map(str, dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]]))
#         print(locations)
#         with open("Duplicates.txt", "at+") as f:
#             f.write(open("Chunks/chunkFile_"+(str(dedupHashTable_SHA256[list(dedupHashTable_SHA256.keys())[k]][0]))+".txt", "r").read()[:-2]+","+("--").join(locations)+"\n")
# f.close()

# # converting text to csv
# import pandas as pd
# df = pd.read_csv("Duplicates.txt", sep=",", header=None)
# df.to_csv("Duplicates.csv", index=False)


# # f.close()
# end_SHA256 = time.time()

# print("Time taken for MD5: ", end_MD5-time_MD5)
# print("Time taken for SHA1: ", end_SHA1-time_SHA1)
# print("Time taken for SHA256: ", end_SHA256-time_SHA256)