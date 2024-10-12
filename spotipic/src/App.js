import './App.css';
import React, { useState, useEffect, useRef } from 'react';
import Header from './Header.js';
import ImageButton from './ImageButton.js';

function App()
{
  // Model Starts Here
  const [isImgAdded, setIsImageAdded] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');


  // Controller starts here

  // Handle file input change
  const handleFileChange = (event) =>
  {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setIsImageAdded(true);  // Indicate that an image has been selected
    }
  };

  // Handle image upload to Flask API
  const handleUpload = async () =>
  {
    if (!selectedFile) {
      alert("Please select an image before uploading.");
      return;
    }
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed!');
      }

      const data = await response.json();
      setUploadStatus(`Upload successful! Image saved at: ${data.image_path}`);
    } catch (error) {
      console.error('Error uploading the image:', error);
      setUploadStatus('Upload failed!');
    }
  };


  // View starts here
  return (
    <div className="App">
      <Header text="Spotipic" textp="Build a spotify playlist based on an image" />
      {/* <ImageButton onImageAdded={handleIsImgAdded} /> */}
      {/* Image upload input */}
      <input type="file" onChange={handleFileChange} />
      {isImgAdded && (
        <button onClick={handleUpload}>Upload Image</button>
      )}

      {/* Display upload status */}
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>

  );
}

export default App;
