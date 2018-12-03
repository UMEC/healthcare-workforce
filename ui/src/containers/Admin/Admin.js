import React, { Component } from 'react';
import { connect } from 'react-redux';

class Admin extends Component {
  render() {
    return (
      <>
        <p>Admin</p>
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