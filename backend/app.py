from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import hashlib
import urllib.request

app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\Arunav\\Desktop\\VTAS_Re\\db'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

Duplic = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def FindDuplicate(FileList):
    # Duplic is in format {hash:[names]}
    global Duplic
    # originalFizeSizes = {file.filename: os.path.getsize(file) for file in FileList}
    # print(originalFizeSizes)
    for file in FileList:
        filename = secure_filename(file.filename)
        # Path to the file
        path = os.path.join(UPLOAD_FOLDER, filename)
        # # Calculate hash
        file = Hash_File(path)
        # Add or append the file path to Duplic
    # print(Duplic)
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

def Hash_File(path):
    # Opening file in afile
    afile = open(path, 'rb')
    blocksize = 4096
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hash = hashlib.md5(buf).hexdigest()
        if hash in Duplic.keys():
            Duplic[hash].append(path)
        else:
            Duplic[hash] = [path]
        buf = afile.read(blocksize)
    afile.close()
    return Duplic


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


# if __name__ == '__main__':
#     app.run(debug=True)
