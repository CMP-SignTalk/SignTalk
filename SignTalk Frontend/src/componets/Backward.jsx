import React, { useEffect } from 'react';
import { TiVideo } from 'react-icons/ti';
import { ReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

import LiveVideoPreview from './LiveVideoPreview';

const Backward = ({ recording, setRecording }) => {
  const [src, setSrc] = React.useState(null);

  useEffect(() => {
    if (src) {
      const audioPlayer = document.getElementById('audio-player');
      audioPlayer.play();
    }
  }, [src]);

  const onStartHandler = () => {
    setRecording(true);
  };

  const onStopHandler = (_, blob) => {
    setRecording(false);
    const file = new File([blob], 'video', { type: blob.type });
    const formData = new FormData();
    formData.append('video', file);
    axios
      .post('http://127.0.0.1:5000/video', formData, {
        responseType: 'arraybuffer',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => {
        const audioData = new Uint8Array(response.data);
        const blob = new Blob([audioData], { type: 'audio/mpeg' });
        const url = URL.createObjectURL(blob);
        setSrc(url);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <div>
      <ReactMediaRecorder
        video
        onStart={onStartHandler}
        onStop={onStopHandler}
        render={({ startRecording, stopRecording, previewStream }) => (
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
            {recording && <LiveVideoPreview stream={previewStream} />}
            {src && <audio controls id='audio-player' src={src}></audio>}
          </div>
        )}
      />
    </div>
  );
};

export default Backward;
