// import logo from './assets/react.svg';

import Avatar from './componets/Avatar';
import Header from './componets/Header';
import Main from './componets/Main';

const App = () => {
  return (
    <div className='h-screen flex flex-col text-signtalk-100'>
      <Header />
      <Main />
      {/* <Avatar/> */}
    </div>
  );
};

export default App;
