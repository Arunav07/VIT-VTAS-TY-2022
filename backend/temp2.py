import hashlib
from flask import Flask, render_template,  request,  jsonify
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\gurve\\My Projects\\Data_Deduplication-VIT-Veritas-\\db'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dedup')
def dedup():
    return render_template('dedup.html')

#global variables    
texts = dict()
AllFiles={}
numberofFiles=0
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    global numberofFiles, AllFiles
    numberofFiles = len(files)
    for file in files:
        Duplic = {}
        total_size = 0
        hashList = []
        hashedSet = set()
        fileR = bytes(file.read())
        chunk_size = 1024
        counter = 0
        currentsize = 0     
        texts = {}
        for i in range(0, len(fileR), chunk_size):
            counter += 1
            currentsize += len(fileR[i:i + chunk_size])
            text = str(fileR[i:i + chunk_size], 'utf-8')
            hashedData = hashlib.md5(fileR[i:i + chunk_size]).hexdigest()
            hashList.append(hashedData)
            hashedSet.add(hashedData)
            texts[hashedData] = text
        Duplic = checkFileDuplicate(hashList, hashedSet, Duplic, texts)
        total_size += currentsize
        Data = createFile(Duplic)
        AllFiles[file.filename] = [Data, total_size]
    return jsonify({'message': 'Success', "Duplic": Data, 'fileSize': currentsize, 'total_size': total_size})
    # return jsonify(AllFiles)


def checkFileDuplicate(hashList, hashedSet, Duplic, texts):        
    for hash in hashedSet:
            Duplic[hash] =hashList.count(hash)
    i=0
    for hash_value, chunk in texts.items():
        os.makedirs('backend/Chunks/Chunks-'+str(i), exist_ok=True)
        with open('backend/Chunks/Chunks-'+str(i)+'/chunk_'+str(i)+'.txt', 'wb+') as chunk_file:
            chunk_file.write(chunk.encode())
        i+=1
    return jsonify(Duplic)


def createFile(Duplic):
<<<<<<< HEAD
    global texts, numberofFiles
    f = open("C:\\Users\\Arunav\\Desktop\\VTAS_Re\\db\\test.txt", "wt+")
    for key, value in texts.items():  
        f.write(texts[key])
    f.close()
    return jsonify({'message': 'Success','fileSize': os.stat("C:\\Users\\Arunav\\Desktop\\VTAS_Re\\backend\\Chunks").st_size, 'Duplic': Duplic, 'texts': texts})
=======
    global total_size, texts
    f = open("C:\\Users\\gurve\\My Projects\\Data_Deduplication-VIT-Veritas-\\db\\test.txt", "wt+")
    for key, value in texts.items():  
        f.write(texts[key])
    f.close()
    print(len(texts), len(Duplic))
    return jsonify({'message': 'Success','fileSize': os.stat("C:\\Users\\gurve\\My Projects\\Data_Deduplication-VIT-Veritas-\\backend\\Chunks").st_size,'total_size': total_size, 'Duplic': Duplic, 'texts': texts})
>>>>>>> temp2

if __name__ == '__main__':
    app.run(debug=True)