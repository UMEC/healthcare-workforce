import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Home from '../Home';
import Admin from '../Admin';
import './App.scss';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
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

export default App;
