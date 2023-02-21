import hashlib
from pathlib import Path
from io import BytesIO
from PIL import Image
from flask import Flask, render_template,  request,  jsonify, make_response
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\gurve\\My Projects\\Data_Deduplication-VIT-Veritas-\\db'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dedup')
def dedup():
    return render_template('dedup.html')


# global variables
DedupData = {}
numberofFiles = 0

@app.route('/upload', methods=['POST'])
def upload():

    files = request.files.getlist('file')
    global numberofFiles, AllFiles
    numberofFiles = len(files)

    print("Files uploaded : ", files)
    print("Number of files uploaded : ", numberofFiles)

    for file in files:
        print(file.filename)
        # Unique_chunks is a dictionary that stores the hash value as key and the chunk content bytes as value . It has the unique hashed value of chunks and its content
        Unique_chunks = {}
        # Duplic is a dictionary that stores the hash value as key and the number of times it occurs as value
        Duplic = {}
        # It is a list of all hash value calculated
        hashList = []
        # hashedSet = set()
        # print(fileR)
        chunk_size = 60
        ShrinkSize = 0
        OriginalSize = 0

        fileR = bytes(file.read())

        [OriginalSize, ShrinkSize, hashList, Duplic, Unique_chunks] = read_file_chunks(fileR, chunk_size, ShrinkSize, OriginalSize, hashList, Duplic, Unique_chunks)
        
        # print ("Hash List : ",hashList)
        print ("Number of unique chunks",len(Unique_chunks))
        # print ("Chunks with their count : ",Duplic)
        print ("Original Size : ",OriginalSize)
        print ("Shrinkage Size :",ShrinkSize)

        createChunks(Unique_chunks, file.filename)
        # createShrinkFile(Unique_chunks, file.filename)  
        DedupData[file.filename] = [OriginalSize, ShrinkSize]

    print("AllFiles : ",DedupData)

    return make_response(jsonify({'message': 'Success', "DedupData": DedupData, 'numberofFiles': numberofFiles}), 200)



def read_file_chunks(fileR, chunk_size, ShrinkSize, OriginalSize, hashList, Duplic, Unique_chunks):

    for i in range(0, len(fileR), chunk_size):
            chunk = fileR[i:i + chunk_size]
            OriginalSize += len(fileR[i:i + chunk_size])
            hashedValue = hashlib.md5(fileR[i:i + chunk_size]).hexdigest()
            hashList.append(hashedValue)

            if Unique_chunks.get(hashedValue) is None:
                ShrinkSize += len(fileR[i:i + chunk_size])

            Unique_chunks[hashedValue] = chunk
            
    for hash in hashList:
        Duplic[hash] = hashList.count(hash)    

    return [OriginalSize,ShrinkSize,hashList,Duplic,Unique_chunks]



def createChunks(Unique_chunks,filename):        
    
    os.makedirs('C:\\Users\\Arunav\\Desktop\\VTAS_Re\\backend\\Chunks_Database\\Chunks-'+filename, exist_ok=True)
    
    i=0
    for hash_value, chunk in Unique_chunks.items():
        with open('C:\\Users\\Arunav\\Desktop\\VTAS_Re\\backend\\Chunks_Database\\Chunks-'+filename+'\\chunk_'+str(i)+'.txt', 'wb+') as chunk_file:
            chunk_file.write(chunk)
        i+=1


    # file_ext = filename.rsplit('.', 1)[1].lower()


    # if file_ext in ['txt']:
    #    for hash_value, chunk in Unique_chunks.items():
    #         chunk = str(bytes(chunk),'utf-8')
    #         with open('backend/Chunks/Chunks-'+filename+'/chunk_'+str(i)+'.'+file_ext, 'wb+') as chunk_file:
    #             chunk_file.write(chunk.encode())
    #         i+=1

    # elif file_ext in ['jpg', 'png']:
    #     for hash_value, chunk in Unique_chunks.items():
    #         image_data = BytesIO(chunk)
    #         img = Image.open(image_data)
    #         img.save('backend/Chunks/Chunks-'+filename+'/chunk_'+str(i)+'.'+file_ext)

            # with open('backend/Chunks/Chunks-'+filename+'/chunk_'+str(i)+'.'+file_ext, 'wb+') as chunk_file:
            #     chunk_file.write(chunk)
            # i+=1

    # elif file_ext in ['mp4', 'avi']:
    #     pass
        


def createShrinkFile(Unique_chunks,filename):
    filename = Path(filename).stem
    f = open("C:\\Users\\gurve\\My Projects\\Data_Deduplication-VIT-Veritas-\\Chunks_Database\\Chunks-"+filename+"\\"+filename+".txt","wb+")
    for hash_value, chunk in Unique_chunks.items():  
        f.write(chunk)
    f.close()

if __name__ == '__main__':
    app.run(debug=True)