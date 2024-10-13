import './App.css';
import React, { useState, useEffect, useRef } from 'react';
import Header from './Header.js';
import i1 from "./Images/Cherry.png";
import i2 from "./Images/Chill.png";
import i3 from "./Images/Cozy.png";
import i4 from "./Images/Genshin.png";
import i5 from "./Images/House.png";
import i6 from "./Images/Lake.png";
import i7 from "./Images/LakeHouse.png";
import i8 from "./Images/Rainbow.png";
import i9 from "./Images/RainyHouse.png";
import i10 from "./Images/Totoro.png";

function App()
{
  // Model Starts Here
  const [isImgAdded, setIsImageAdded] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  // Refs for DOM elements
  const trackRef = useRef(null);


  // Controller starts here

  const handleOnDown = (e) =>
  {
    if (trackRef.current) {
      trackRef.current.dataset.mouseDownAt = e.clientX;
    }
  };

  const handleOnUp = () =>
  {
    if (trackRef.current) {
      trackRef.current.dataset.mouseDownAt = "0";
      trackRef.current.dataset.prevPercentage = trackRef.current.dataset.percentage;
    }
  };

  const handleOnMove = (e) =>
  {
    if (!trackRef.current || trackRef.current.dataset.mouseDownAt === "0") return;

    const mouseDelta = parseFloat(trackRef.current.dataset.mouseDownAt) - e.clientX;
    const maxDelta = window.innerWidth / 2;

    const percentage = (mouseDelta / maxDelta) * -100;
    const nextPercentageUnconstrained = parseFloat(trackRef.current.dataset.prevPercentage) + percentage;
    const nextPercentage = Math.max(Math.min(nextPercentageUnconstrained, 0), -100);

    trackRef.current.dataset.percentage = nextPercentage;

    trackRef.current.animate(
      {
        transform: `translate(${nextPercentage - 5.5}%, -20%)`,
      },
      { duration: 1200, fill: "forwards" }
    );

    // Animate each image inside the track
    for (const image of trackRef.current.getElementsByClassName("image")) {
      image.animate(
        {
          objectPosition: `${100 + nextPercentage}% center`,
        },
        { duration: 1200, fill: "forwards" }
      );
    }
  };

  // Handle file input change
  const handleFileChange = (event) =>
  {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setIsImageAdded(true); // Indicate that an image has been selected
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

  // UseEffect to manage mouse/touch event listeners
  useEffect(() =>
  {
    // Bind event listeners for mouse and touch interactions
    window.onmousedown = handleOnDown;
    window.ontouchstart = (e) => handleOnDown(e.touches[0]);
    window.onmouseup = handleOnUp;
    window.ontouchend = (e) => handleOnUp(e.touches[0]);
    window.onmousemove = handleOnMove;
    window.ontouchmove = (e) => handleOnMove(e.touches[0]);

    // Cleanup event listeners when the component is unmounted
    return () =>
    {
      window.onmousedown = null;
      window.ontouchstart = null;
      window.onmouseup = null;
      window.ontouchend = null;
      window.onmousemove = null;
      window.ontouchmove = null;
    };
  }, []); // Empty dependency array ensures these event listeners are set once

  return (
    <div className="App" id="background-gradient">
      <Header textp="Upload an image to turn it into a song!" />

      <div className="inputs">
        <input type="file" onChange={handleFileChange} />
        {isImgAdded && (
          <button onClick={handleUpload}>Upload Image</button>
        )}
        {uploadStatus && <p>{uploadStatus}</p>}
      </div>

      {/* Image track */}
      {isImgAdded && (
        <div
          id="image-track"
          ref={trackRef}
          data-mouse-down-at="0"
          data-prev-percentage="0"
        >
          <img className="image" src={i1} draggable="false" alt="1" />
          <img className="image" src={i2} draggable="false" alt="2" />
          <img className="image" src={i3} draggable="false" alt="3" />
          <img className="image" src={i4} draggable="false" alt="4" />
          <img className="image" src={i5} draggable="false" alt="5" />
          <img className="image" src={i6} draggable="false" alt="6" />
          <img className="image" src={i7} draggable="false" alt="7" />
          <img className="image" src={i8} draggable="false" alt="8" />
          <img className="image" src={i9} draggable="false" alt="9" />
          <img className="image" src={i10} draggable="false" alt="10" />
        </div>
      )}
    </div>
  );
}

export default App;
