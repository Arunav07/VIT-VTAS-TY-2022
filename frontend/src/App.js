import React, { useState } from 'react';

function App() {
  const [fileList, setFileList] = useState(null);

  const handleFileChange = (event) => {
    setFileList(event.target.files);
  }

  const handleUpload = (event) => {
    // event.preventDefault();
    if (!fileList) {
      return;
    }

    const formData = new FormData();
    files.forEach((file, i) => {
      formData.append(`file-${i}`, file, file.name);
    });
    // formData.append('file', file);
    console.log(formData);
    localStorage.setItem("Formdata",JSON.stringify(formData));


    fetch('https://httpbin.org/post', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      try {
        // JSON.parse(data);
        console.log('Success:', data);
    }
    catch (error) {
        console.log('Error parsing JSON:', error, data);
    }
    })
    .catch(error => {
      console.error(error);
    });
  }
  
  const files = fileList ? [...fileList] : [];
  
  return (
    <div className="App">
      <h2>File Upload</h2>
      <form>
        <span className="uploadContainer">
          <label htmlFor="file">Choose a file: </label>
          <input type="file" id="file" onChange={handleFileChange} multiple/>
        </span>

        <ul>
        {files.map((file, i) => (
          <li key={i}>
            {file.name} - {file.type}
          </li>
        ))}
      </ul>

        <button className="uploadButton" type='submit' onClick={(e)=>{
          handleUpload(e);
          console.log(files)
        }} >Upload</button>
      </form>
    </div>
  );
}

export default App;
