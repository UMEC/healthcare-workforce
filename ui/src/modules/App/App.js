import React, { Component } from 'react';
import { connect } from 'react-redux';
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

import {
  INITIAL_MODEL_INFO_REQUEST
} from '../../actions';

import './App.scss';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      response: '',
    }
  }

  componentDidMount() {
    this.props.onRequestAnalyticsIds();
  }
  
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

const mapDispatchToProps = dispatch => {
  return {
    onRequestAnalyticsIds: () => dispatch({ type: INITIAL_MODEL_INFO_REQUEST })
  }
};

export default connect(null, mapDispatchToProps)(App);
