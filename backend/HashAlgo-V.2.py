from flask import Flask, render_template, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import hashlib
Duplic = {}

app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\Arunav\\Desktop\\VTAS_Re\\db'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

file_locations = {}
total_sizes = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dedup')
def dedup():
    return render_template('dedup.html')

@app.route('/upload', methods=['POST'])
def upload():
    global file_locations, total_sizes
    files = request.files.getlist('file')
    for file in files:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        total_sizes += os.path.getsize(filepath)
        # read file and calculate the hash
        file_hash = MD5Hash(filepath)

        if file_hash in file_locations:
            file_locations[file_hash].append(filepath)
        else:
            file_locations[file_hash] = [filepath]
    return jsonify({'message': 'Success', 'size': len(file_locations), 'file_locations': file_locations, 'total_size': total_sizes,'fileSize': os.path.getsize(file_locations[file_hash][0])})

def MD5Hash(file):
    chunk_size = 1024
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read(1024)
        hasher.update(buf)
    return hasher.hexdigest()

def hashFiles(file):
    blocksize = 1024
    buf = bytes(file.read(blocksize))
    while True:
        hash = hashlib.md5(buf).hexdigest()
        if hash in Duplic.keys():
            Duplic[hash].append(file.filename)
        else:
            Duplic[hash] = [file.filename]
        buf = bytes(file.read(blocksize))

if __name__=='__main__':
    app.run(debug=True)