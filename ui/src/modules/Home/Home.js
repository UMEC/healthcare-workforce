import React, { Component } from 'react';
// import { bindActionCreators } from 'redux';
import {
  GET_ANALYTICS_IDS_REQUEST
} from '../../actions';

import { connect } from 'react-redux';

class Home extends Component {
  componentDidMount() {
    this.props.onRequestAnalyticsIds();
  }

  render() {
    let { defaultModel } = this.props;
    return (
      <>
        <p>Home</p>
        <p>{defaultModel}</p>
      </>
    );
  }
}

function mapStateToProps(state) {
  return {
    defaultModelData: state.defaultModelData,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onRequestAnalyticsIds: () => dispatch({ type: GET_ANALYTICS_IDS_REQUEST })
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);