import React, { Component } from 'react';
// import { bindActionCreators } from 'redux';

import { connect } from 'react-redux';

class Home extends Component {
  componentDidMount() {
    // this.props.onRequestAnalyticsIds();
  }

  render() {
    let { modelId } = this.props.model;
    return (
      <>
        <p>Home</p>
        <p>{modelId}</p>
      </>
    );
  }
}

function mapStateToProps(state) {
  return {
    model: state.model,
  }
}

export default connect(mapStateToProps)(Home);