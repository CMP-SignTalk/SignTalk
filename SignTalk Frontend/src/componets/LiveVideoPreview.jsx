import React, { useEffect, useRef } from 'react';

const LiveVideoPreview = ({ stream }) => {
  const videoRef = useRef();
  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);
  if (!stream) {
    return null;
  }
  return <video ref={videoRef} width={300} height={300} autoPlay controls />;
};

export default LiveVideoPreview;
