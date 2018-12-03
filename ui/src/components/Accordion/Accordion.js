import React, { Component } from 'react'
/** 
 * this is the Accordion Component
 * 
 * @author [@domwashburn](https://github.com/domwashburn)
 */
class Accordion extends Component {
  constructor(props) {
    super(props);

    const openSections = {};

    this.state = {
      openSections,
    }
  }

  /** 
   * The click event handler for the accordion label
   * 
   * @param {}
   * @public
   */
  onClick = label => {
    const { state: { openSections } } = this;

    // Coerce a boolean value
    const isOpen = !!openSections[label];

    this.setState({ 
      openSections: { 
        ...this.state.openSections,
        [label]: !isOpen 
      }
    })
  }

  /**
   * Adds props necessary for accordion functionality to child components
   * These are used to maintain state within the accordion parent
   * 
   * @param {Object} child a React child, pulled from this.props.children
   * @param {{ onClick: fn, isOpen: boolean }} accordionSectionProps  Object containing props to pass down to each child
   * 
   * @private
   */
  addAccordionPropsToChild = (child, accordionSectionProps) => {
    return React.cloneElement(child, accordionSectionProps)
  } 

  render() {
    const { state: { openSections } } = this;

    return (
      <div className="accordion">
        {this.props.children.map( child => {

          /** Object containing props to pass to pass down to child components */
          const accordionSectionProps = {
            /**  */
            onClick: this.onClick,
            isOpen: !!openSections[child.props.label],
          };

          return this.addAccordionPropsToChild(child, accordionSectionProps);
        })}
      </div>
    );
  }
}

export default Accordion