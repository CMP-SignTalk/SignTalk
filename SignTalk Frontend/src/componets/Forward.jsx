import React, { useState } from 'react';
import { MdKeyboardVoice } from 'react-icons/md';
import { ReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

const Forward = ({ recording, setRecording }) => {
  const [gloss, setGloss] = useState(null);
  const [transcript, setTranscript] = useState(null);

  const onStopHandler = (blobUrl, blob) => {
    const file = new File([blob], 'audio.webm', { type: 'audio/wav' });
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
        setGloss(res.data.aslg);
        setTranscript(res.data.transcript);
      })
      .catch((err) => {
        console.log(err);
      });
    setRecording(false);
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
          <div className="flex flex-col justify-center items-center">
            <button
              className="btn"
              onClick={recording ? stopRecording : startRecording}
            >
              <span className="mr-2">
                <MdKeyboardVoice />
              </span>
              {recording ? 'Stop' : 'Start'} Recording
            </button>
            {transcript && (
              <div className="flex flex-row">
                <label htmlFor="transcript">Transcript: </label>
                &nbsp;&nbsp;&nbsp;
                <p id="transcript">{transcript}</p>
              </div>
            )}
            {gloss && (
              <div className="flex flex-row">
                <label htmlFor="gloss">Glosses: </label>
                &nbsp;&nbsp;&nbsp;
                <p id="gloss">{gloss}</p>
              </div>
            )}
          </div>
        )}
      />
    </div>
  );
};

export default Forward;
