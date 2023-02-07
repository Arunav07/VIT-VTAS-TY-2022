from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import hashlib
import urllib.request
import binascii

app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/gurve/My Projects/Data_Deduplication-VIT-Veritas-/db'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
Duplic = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def FindDuplicate(FileList):

    # Duplic is in format {hash:[names]}
    Duplic = {}
    for file in FileList:
        filename = secure_filename(file.filename)
        # Path to the file
        path = os.path.join(UPLOAD_FOLDER, filename)

        # Calculate hash
        file_hash = Hash_File(path)
        # print(path,file_hash)

        # Add or append the file path to Duplic
        if file_hash in Duplic:
            Duplic[file_hash].append(filename)
        else:
            Duplic[file_hash] = [filename]

    print(Duplic)

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
    # hex_data = binascii.hexlify(file)
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            # if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        d = FindDuplicate(files)
        Join_Dictionary(Duplic, d)
        results = list(filter(lambda x: len(x) > 1, Duplic.values()))
        print(results)

        for dup_list in results :
            for j in range(1,len(dup_list)) :
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, dup_list[j]))
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

        flash('File(s) successfully uploaded')
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
