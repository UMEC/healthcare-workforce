import React, {Component} from 'react';
import { connect } from 'react-redux';

class UserInfo extends Component {
  render() {
    return <p>{this.props.user.name}</p>
  }
}

function mapStateToProps( state ) {
  return {
    user: state.user,
  }
}

export default connect(mapStateToProps)(UserInfo);