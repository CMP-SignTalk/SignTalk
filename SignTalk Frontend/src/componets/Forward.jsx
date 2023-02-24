import React from 'react';
import { MdKeyboardVoice } from 'react-icons/md';
import { ReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

let flag = false;

const Forward = ({ recording, setRecording }) => {
  const onStopHandler = (blobUrl, blob) => {
    const file = new File([blob], 'audio', { type: blob.type });
    // Send the audio file to the backend server for processing
    const formData = new FormData();
    formData.append('audio', file);
    axios
      .post('http://127.0.0.1:5000/audio', formData, {
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
    flag = true;
  };
  return (
    <div>
      <ReactMediaRecorder
        audio
        onStart={() => {
          setRecording(true);
        }}
        onStop={onStopHandler}
        render={({ startRecording, stopRecording, mediaBlobUrl }) => (
          <div className='flex flex-col justify-center items-center'>
            <button
              className='btn'
              onClick={recording ? stopRecording : startRecording}
            >
              <span className='mr-2'>
                <MdKeyboardVoice />
              </span>
              {recording ? 'Stop' : 'Start'} Recording
            </button>
            {flag && <audio src={mediaBlobUrl} controls autoPlay />}
          </div>
        )}
      />
    </div>
  );
};

export default Forward;
