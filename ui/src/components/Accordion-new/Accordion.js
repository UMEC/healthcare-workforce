import React, { Component } from 'react'

class Accordion extends Component {
  constructor(props) {
    super(props);

    const openSections = {};

    this.state = {
      openSections,
    }
  }

  componentDidUpdate(nextProps, nextState) {
    console.log(this.state);
  }

  onClick = label => {
    const { state: { openSections } } = this;

    const isOpen = !!openSections[label];

    this.setState({ 
      openSections: { 
        ...this.state.openSections,
        [label]: !isOpen 
      }
    })
  }

  render() {
    const { state: { openSections } } = this;
    return (
      <div className="accordion">
        {this.props.children.map( child => {
          return React.cloneElement( child, {
            onClick: this.onClick,
            isOpen: !!openSections[child.props.label],
          })
        })}
      </div>
    );
  }
}

export default Accordion