import React, { Component } from 'react';
// import { bindActionCreators } from 'redux';

import { connect } from 'react-redux';

class Home extends Component {
  componentDidMount() {
    // this.props.onRequestAnalyticsIds();
  }

  render() {
    let { modelId } = this.props.defaultModel;
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
    defaultModel: state.defaultModel,
  }
}

export default connect(mapStateToProps)(Home);