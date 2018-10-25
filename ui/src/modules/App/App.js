import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Home from '../Home';
import Admin from '../Admin';

//Components
import AppHeader from '../../components/AppHeader';
import ViewHeader from '../../components/ViewHeader';
import AppContent from '../../components/AppContent';
import ViewContainer from '../../components/ViewContainer';
import ViewFooter from '../../components/ViewFooter';
import Panel from '../../components/Panel';

import './App.scss';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      response: '',
    }
  }
  
  // componentDidMount() {
  //   this.callApi()
  //     .then(res => this.setState({ response: res[0].name }))
  //     .catch(err => console.log(err));
  // }

  // callApi = async () => {
  //   const response = await fetch('/api/source');
  //   const body = await response.json();

  //   if (response.status !== 200) throw Error(body.message);
  //   console.log("Received body: " + body);
  //   return body;
  // };

  componentDidMount() {
    this.callAnalyticsPostApi()
      .then(res => {
        this.callAnalyticsGetApi(res.modelId).then(res2 => {
          this.setState({ response: JSON.stringify(res2) })
        })
      })
      .catch(err => console.log(err));
  }

  callAnalyticsPostApi = async () => {
    const response = await fetch('/api/analytics', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "params": { "type": "cost_quality_adjustment", "value": 0.5 } })
    });

    const body = await response.json();

    if (response.status !== 200) throw Error(body.message);
    console.log("Post respnse: " + JSON.stringify(body));
    return body;
  };

  callAnalyticsGetApi = async (modelId) => {
    const response = await fetch('/api/analytics/' + modelId, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    });

    const body = await response.json();

    if (response.status !== 200) throw Error(body.message);
    console.log("Get response: " + JSON.stringify(body));
    return body;
  };
  
  render() {
    return (
      <Router>
        <div className="container">
          <AppHeader>
            <div className="branding">

            </div>
            <MainNavigation />
          </AppHeader>
          <AppContent>
            <ViewContainer>
              <ViewHeader />
              <Route exact path="/" component={Home} />
              <Route exact path="/admin" component={Admin} />
              <p className="App-intro">{this.state.response}</p>
              Main Content Area
              <ViewFooter />
            </ViewContainer>
            <Panel />
          </AppContent>
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
