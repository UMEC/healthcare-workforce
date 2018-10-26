import React, { Component } from 'react';
// import { bindActionCreators } from 'redux';
import {
  MODEL_INFO_REQUEST
} from '../../actions';

import { connect } from 'react-redux';

class Home extends Component {
  componentDidMount() {
    this.props.onRequestAnalyticsIds();
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

const mapDispatchToProps = dispatch => {
  return {
    onRequestAnalyticsIds: () => dispatch({ type: MODEL_INFO_REQUEST })
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);