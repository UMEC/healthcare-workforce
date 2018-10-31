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
        <div>
          <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
            <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">UMEC Gap Analysis Tool</a>
            <ul class="navbar-nav px-3">
              <li class="nav-item text-nowrap">
                <a class="nav-link" href="/">Home</a>
              </li>
            </ul>
          </nav>
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
