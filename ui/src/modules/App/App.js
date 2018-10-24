import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Home from '../Home';
import Admin from '../Admin';
import './App.scss';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      response: '',
    }
  }
  
  componentDidMount() {
    this.callApi()
      .then(res => this.setState({ response: res[0].name }))
      .catch(err => console.log(err));
  }

  callApi = async () => {
    const response = await fetch('/api/source');
    const body = await response.json();

    if (response.status !== 200) throw Error(body.message);
    console.log("Received body: " + body);
    return body;
  };
  
  render() {
    return (
      <Router>
        <div className="App">
          <MainNavigation />
          <Route exact path="/" component={Home} />
          <Route exact path="/admin" component={Admin} />
          <p className="App-intro">{this.state.response}</p>
        </div>
      </Router>
    );
  }
}

// Temp

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
