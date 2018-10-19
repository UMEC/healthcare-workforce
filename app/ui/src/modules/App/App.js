import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import logo from '../../assets/images/logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p>
              Edit <code>src/App.js</code> and save to reload.
            </p>
            <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn React
            </a>
          </header>
          <MainNavigation />
          <Route exact path="/" component={Home} />
          <Route exact path="/admin" component={Admin} />
        </div>
      </Router>
    );
  }
}

// Temp 👇

let MainNavigation = () => {
  return (
    <nav>
      <Link to="/" >
        <button>Home</button>
      </Link>
      <Link to="/admin" >
        <button>Admin</button>
      </Link>
    </nav>
  )
};

let Home = () => {
  return (
    <p>Home</p>
  );
};

let Admin = () => {
  return (
    <p>Super Secret Admin</p>
  );
};

export default App;
