import hashlib
from flask import Flask, render_template,  request,  jsonify, make_response
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
AllFiles={}
numberofFiles=0
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    global numberofFiles, AllFiles
    numberofFiles = len(files)
    # print("Files uploaded : ",files)
    # print("Number of files uploaded : ",numberofFiles)
    for file in files:
        # print(file.filename)
        #Unique_chunks is a dictionary that stores the hash value as key and the chunk content as value . It has the unique hashed value of chunks and its content
        Unique_chunks = {}
        #Duplic is a dictionary that stores the hash value as key and the number of times it occurs as value
        Duplic = {}
        #It is a list of all hash value calculated
        hashList = []
        # hashedSet = set()
        # print(fileR)
        chunk_size = 600
        counter = 0
        ShrinkSize = 0
        OriginalSize = 0 

        fileR = bytes(file.read())
        
        for i in range(0, len(fileR), chunk_size):
            counter += 1
            chunk = str(bytes(fileR[i:i + chunk_size]),'utf-8')
            OriginalSize += len(fileR[i:i + chunk_size])
            hashedValue = hashlib.md5(fileR[i:i + chunk_size]).hexdigest()
            hashList.append(hashedValue)
            # hashedSet.add(hashedValue)

            if Unique_chunks.get(hashedValue) is None:
                ShrinkSize += len(fileR[i:i + chunk_size])

            Unique_chunks[hashedValue] = chunk
        
        for hash in hashList:
            Duplic[hash] = hashList.count(hash)
        
        # print (hashList)
        # print (hashedSet)
        # print (len(Unique_chunks))
        # print (Duplic)
        # print ("Original Size : ",OriginalSize)
        # print ("Shrinkage Size :",ShrinkSize)

        createChunks(Unique_chunks,file.filename)
        createShrinkFile(Unique_chunks,file.filename) # Data = dictionary()
        AllFiles[file.filename] = [OriginalSize,ShrinkSize]

    
    # print("AllFiles",AllFiles)
    
    return make_response(jsonify({'message': 'Success', "AllFiles": AllFiles, 'numberofFiles': numberofFiles}), 200)


def createChunks(Unique_chunks,filename):        
    
    i=0
    os.makedirs('backend/Chunks/Chunks-'+filename, exist_ok=True)
    for hash_value, chunk in Unique_chunks.items():
        with open('backend/Chunks/Chunks-'+filename+'/chunk_'+str(i)+'.txt', 'wb+') as chunk_file:
            chunk_file.write(chunk.encode())
        i+=1


def createShrinkFile(Unique_chunks,filename):
    f = open("C:\\Users\\gurve\\My Projects\\Data_Deduplication-VIT-Veritas-\\backend\\Chunks\\Chunks-"+filename+"\\"+filename,"wt+")
    for hash_value, chunk in Unique_chunks.items():  
        f.write(chunk)
    f.close()

if __name__ == '__main__':
    app.run(debug=True)