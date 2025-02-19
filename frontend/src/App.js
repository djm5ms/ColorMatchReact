import logo from './logo.svg';
import './App.css';

function myButton()
{
  return (
    <button>Click me!</button>
  );
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        This is my first React app!
      </header>
      <body>
      {myButton()}
    </body>
    </div>
    
  );
}



export default App;
