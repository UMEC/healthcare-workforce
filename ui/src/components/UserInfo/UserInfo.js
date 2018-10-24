import React, {Component} from 'react';

class UserInfo extends Component {
  render() {
    return <p>{this.props.children}</p>
  }
}

export default UserInfo;