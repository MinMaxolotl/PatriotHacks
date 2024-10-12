import './App.css';
import React, { useState, useEffect, useRef } from 'react';
import Header from './Header.js';
import ImageButton from './ImageButton.js';

function App()
{
  // const [currentTime, setCurrentTime] = useState(0);
  // useEffect(() =>
  // {
  //   fetch('/time').then(res => res.json()).then(data =>
  //   {
  //     setCurrentTime(data.time);
  //   })
  // }, [])

  // Model starts here
  const [isImgAdded, setIsImageAdded] = useState(false);

  const [stream, setStream] = useState(null);
  const videoRef = useRef(null);
  useEffect(() =>
  {
    const getMedia = async () =>
    {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        });
        setStream(mediaStream);
      } catch (error) {
        console.error('Error accessing media devices:', error);
      }
    };

    getMedia();
  }, []);
  useEffect(() =>
  {
    if (stream && videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  // Controller starts here

  function handleIsImgAdded()
  {
    setIsImageAdded(current => !current);
  }

  // View starts here
  return (
    <div className="App">
      <Header text="Spotipic" textp="Build a spotify playlist based on an image" />
      <ImageButton
        onImageAdded={handleIsImgAdded} />
      <video ref={videoRef} autoPlay playsInline />
    </div>

  );
}

export default App;
