import React, { Component } from 'react';
import { connect } from 'react-redux';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import ModelOutputContainer from '../../containers/ModelOutputContainer/ModelOutputContainer';

//Components
import AppContent from '../../components/AppContent';
import AppHeader from '../../components/AppHeader';


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
          </AppHeader>
          <AppContent>
            <Route exact path="/" component={ModelOutputContainer} />
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
    </nav>
  )
};

const mapDispatchToProps = dispatch => {
  return {
    onRequestAnalyticsIds: () => dispatch({ type: INITIAL_MODEL_INFO_REQUEST })
  }
};

export default connect(null, mapDispatchToProps)(App);
