import React from 'react';
import { TiVideo } from 'react-icons/ti';
import { ReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

import LiveVideoPreview from './LiveVideoPreview';

let flag = false;

const Backward = ({ recording, setRecording }) => {
  const onStopHandler = (blobUrl, blob) => {
    const file = new File([blob], 'video', { type: blob.type });
    // Send the video file to the backend server for processing
    const formData = new FormData();
    formData.append('video', file);
    axios
      .post('http://127.0.0.1:5000/video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
    setRecording(false);
  };
  return (
    <div>
      <ReactMediaRecorder
        video
        onStart={() => {
          setRecording(true);
          flag = true;
        }}
        onStop={onStopHandler}
        render={({
          startRecording,
          stopRecording,
          previewStream,
          mediaBlobUrl,
        }) => (
          <div className='flex flex-col justify-center items-center'>
            <button
              className='btn'
              onClick={recording ? stopRecording : startRecording}
            >
              <span className='mr-2'>
                <TiVideo />
              </span>
              {recording ? 'Stop' : 'Start'} Recording
            </button>
            {recording ? (
              <LiveVideoPreview stream={previewStream} />
            ) : (
              flag && (
                <video
                  src={mediaBlobUrl}
                  controls
                  autoPlay
                  width={300}
                  height={300}
                />
              )
            )}
          </div>
        )}
      />
    </div>
  );
};

export default Backward;
