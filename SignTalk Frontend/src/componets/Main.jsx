import React, { useState } from 'react';
// import { AiOutlineSwap,  } from 'react-icons/ai';
import { MdSwapHorizontalCircle } from 'react-icons/md';
// import { HiArrowPath } from 'react-icons/hi';
import { IoMdSwap } from 'react-icons/io';

import Forward from './Forward';
import Backward from './Backward';

const Main = () => {
  const [isForward, setIsForward] = useState(true);
  const [recording, setRecording] = useState(false);

  return (
    <main className='flex-1 flex flex-col justify-between py-8 items-center bg-signtalk-100 text-signtalk-800'>
      <h2 className='text-2xl text-signtalk-800 font-bold'>
        {`${isForward ? 'English' : 'ASL'} to ${isForward ? 'ASL' : 'English'}`}
      </h2>
      {isForward ? (
        <Forward recording={recording} setRecording={setRecording} />
      ) : (
        <Backward recording={recording} setRecording={setRecording} />
      )}
      <button
        disabled={recording}
        onClick={() => {
          setIsForward(!isForward);
        }}
        className='btn disabled:opacity-50 disabled:cursor-not-allowed'
      >
        {`Press for ${isForward ? 'ASL' : 'English'} to ${
          isForward ? 'English' : 'ASL'
        }`}
      </button>
    </main>
  );
};

export default Main;
