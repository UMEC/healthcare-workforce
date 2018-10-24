import React, { Component } from 'react';
import { connect } from 'react-redux';
import UserInfo from '../../components/UserInfo';

class Admin extends Component {
  render() {
    return (
      <>
        <p>Admin</p>
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

export default connect(mapStateToProps)(Admin);