import hashlib
from flask import Flask, render_template,  request,  jsonify, make_response
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\Arunav\\Desktop\\VTAS_Re\\db'

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
AllFiles={}
numberofFiles=0
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    print(files)
    global numberofFiles, AllFiles
    numberofFiles = len(files)
    print(numberofFiles)
    for file in files:
        texts = dict()
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
            text = str(bytes(fileR[i:i + chunk_size]),'utf-8')
            hashedData = hashlib.md5(fileR[i:i + chunk_size]).hexdigest()
            hashList.append(hashedData)
            hashedSet.add(hashedData)
            texts[hashedData] = text
        
        #Duplic is a dictionary that stores the hash value as key and the number of times it occurs as value
        #texts is a dictionary that stores the hash value as key and the chunk as value

        Duplic = checkFileDuplicate(hashList, hashedSet, Duplic, texts)
        # total_size += currentsize
        Data = createFile(Duplic, texts) # Data = dictionary()
        AllFiles[file.filename] = [Data, currentsize]
        print(AllFiles)
    AllFiles['numberofFiles'] = numberofFiles
    return make_response(jsonify({'message': 'Success', "Duplic": AllFiles, 'fileSize': currentsize}), 200)


def checkFileDuplicate(hashList, hashedSet, Duplic, texts):        
    for hash in hashedSet:
            Duplic[hash] =hashList.count(hash)
    # size = len(Duplic)*1024
    # Duplic["size"] = size
    i=0
    for hash_value, chunk in texts.items():
        os.makedirs('backend/Chunks/Chunks-'+str(i), exist_ok=True)
        with open('backend/Chunks/Chunks-'+str(i)+'/chunk_'+str(i)+'.txt', 'wb+') as chunk_file:
            chunk_file.write(chunk.encode())
        i+=1
    return Duplic


def createFile(Duplic, texts):
    f = open("C:\\Users\\Arunav\\Desktop\\VTAS_Re\\db\\test.txt", "wt+")
    for key, value in texts.items():  
        f.write(texts[key])
    f.close()
    return {'message': 'Success','fileSize': os.stat("C:\\Users\\Arunav\\Desktop\\VTAS_Re\\db\\test.txt").st_size, 'Duplic': Duplic, 'texts': texts}

if __name__ == '__main__':
    app.run(debug=True)