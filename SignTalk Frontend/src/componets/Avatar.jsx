import React, { useState } from 'react';

import Forward from './Forward';
import Backward from './Backward';

const Avatar = () => {

  return (
    <main >
     <iframe mozallowfullscreen="true" allow="autoplay; fullscreen"
        src="http://127.0.0.1:5500/web_build4/index.html" 
        name="Pong: Star Wars Remix" scrolling="no" msallowfullscreen="true" 
        allowFullScreen={true} webkitallowfullscreen="true" allowtransparency="true"
        frameBorder="0" marginHeight="px" marginWidth="320px" height="540px"  
        width="960px"></iframe>
    </main>
  );
};


export default Avatar;
