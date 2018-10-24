import React, { Component } from 'react';
import { connect } from 'react-redux';
import UserInfo from '../../components/UserInfo';

class Home extends Component {
  render() {
    return (
      <>
        <p>Home</p>
        <UserInfo>{this.props.user.name}</UserInfo>
      </>
    );
  }
}

function mapStateToProps(state) {
  return {
    user: state.user,
  }
}

export default connect(mapStateToProps)(Home);