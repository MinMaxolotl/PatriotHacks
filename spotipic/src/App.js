import './App.css';
import React, { useState, useEffect, useRef } from 'react';
import Header from './Header.js';
import i1 from "./Images/Cherry.png"; // Default image imports (for testing)
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
  // Model starts here
  const [isImgAdded, setIsImageAdded] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [imageData, setImageData] = useState([]);
  const [loading, setLoading] = useState(false); // For loading state

  // Refs for DOM elements
  const trackRef = useRef(null);

  // Handle file input change
  const handleFileChange = (event) =>
  {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setIsImageAdded(true); // Indicate that an image has been selected
    }
  };

  const handleUpload = async () =>
  {
    if (!selectedFile) {
      alert("Please select an image before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    setLoading(true); // Start loading

    try {
      const response = await fetch('http://127.0.0.1:5000/upload-image', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const jsonData = await response.json();  // Directly parse JSON

        console.log("Json Stuff" + jsonData); // Log the response to verify

        if (jsonData.mapThisString) {
          // Map the JSON data to the required format
          const formattedData = jsonData.mapThisString.map((track) => ({
            name: track.track_name,
            artist: track.artist,
            linkToSong: track.spotify_link, // Add the spotify link
            linkToImage: track.album_image, // Use the image URL for the image src
          }));
          setImageData(formattedData);  // Set the image data in the state
          console.log("Formatted" + formattedData)
          setUploadStatus('Upload successful!');
        } else {
          setUploadStatus('Error: No mapThisString data found.');
        }

      } else {
        setUploadStatus('Failed to upload image.');
      }
    } catch (error) {
      console.error('Error uploading the image:', error);
      setUploadStatus('Upload failed!');
    } finally {
      setLoading(false);  // Stop loading
    }
  };


  // Controller for mouse and touch events
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
    for (const image of trackRef.current.getElementsByClassName("time2")) {
      image.animate(
        {
          objectPosition: `${100 + nextPercentage}% center`,
        },
        { duration: 1200, fill: "forwards" }
      );
    }
  };

  // UseEffect to manage mouse/touch event listeners
  useEffect(() =>
  {
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
  }, []);

  return (
    <div className="App" id="background-gradient">
      <Header textp="Upload an image to turn it into a song!" />

      <div className="inputs">
        <input type="file" onChange={handleFileChange} />
        {isImgAdded && !loading && (
          <button onClick={handleUpload}>Upload Image</button>
        )}
        {uploadStatus && <p>{uploadStatus}</p>}
        {loading && <p>Loading...</p>}
      </div>
      <div id="image-track"
        ref={trackRef}
        data-mouse-down-at="0"
        data-prev-percentage="0">
        {/* Render images dynamically from the API response */}
        {imageData.map((image, index) => (
          <div key={index} className="time">
            <a href={image.linkToSong} className="image" target="_blank" draggable="false">
              <img className="time2" src={image.linkToImage} alt={image.name} draggable="false" />
            </a>
          </div>
        ))}
      </div>
    </div >
  );
}

export default App;
