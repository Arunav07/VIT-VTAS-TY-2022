import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  }

  const handleUpload = (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    fetch('/server/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      try {
        JSON.parse(data);
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
  
  return (
    <div className="App">
      <h2>File Upload</h2>
      <form>
        <span className="uploadContainer">
          <label htmlFor="file">Choose a file: </label>
          <input type="file" id="file" onChange={handleFileChange}/>
        </span>
        <button className="uploadButton" type='submit' onClick={(e)=>{
          handleUpload(e);
          console.log(file)
        }} >Upload</button>
      </form>
    </div>
  );
}

export default App;
