import os
from pathlib import Path
import hashlib


def FindDuplicate(SupFolder):

    # Duplic is in format {hash:[names]}
    Duplic = {}
    for file_name in files:

        # Path to the file
        path = os.path.join(folders, file_name)

        # Calculate hash
        file_hash = Hash_File(path)
        # print(path,file_hash)

        # Add or append the file path to Duplic
        if file_hash in Duplic:
            Duplic[file_hash].append(file_name)
        else:
            Duplic[file_hash] = [file_name]

    print (Duplic)
    
    return Duplic

# Joins dictionaries

def Join_Dictionary(dict_1, dict_2):
    for key in dict_2.keys():

        # Checks for existing key
        if key in dict_1:

            # If present Append
            dict_1[key] = dict_1[key] + dict_2[key]
        else:

            # Otherwise Stores
            dict_1[key] = dict_2[key]


# Calculates MD5 hash of file
# Returns HEX digest of file

def Hash_File(path):

    # Opening file in afile
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    blocksize = 65536
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


Duplic = {}
folders = Path('C:/Users/gurve/My Projects/Data_Deduplication-VIT-Veritas-/Test_dir')
files = sorted(os.listdir(folders))
         
for i in files:
    # Iterate over the files
    # Find the duplicated files
    # Append them to the Duplic
Join_Dictionary(Duplic, FindDuplicate(files))

# Results store a list of Duplic values
results = list(filter(lambda x: len(x) > 1, Duplic.values()))

print (results)

if len(results) > 0:
    for result in results:
        for sub_result in result:
            print('\t\t%s' % sub_result)
else:
    print('No duplicates found.')

