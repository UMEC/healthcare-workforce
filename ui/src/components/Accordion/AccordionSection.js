import React, {Component} from 'react';
import PropTypes from 'prop-types';
import _ from 'lodash';

/** 
 * The `<AccordionSection>` component
 */
class AccordionSection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      containerHeight: 0,
    }
  }

  handleLabelClick = () => {
    this.props.onClick(this.props.label)
  }


  render() {
    let { isOpen } = this.props;
    let openClassName = isOpen ? 'is-open' : 'is-closed';

    return (
      <div className="accordion__section">
        <AccordionSectionHeader 
          openClassName={openClassName}
          onClick={() => this.handleLabelClick()}>

          {/* <div class="accordion__trigger-icon">
            {`{CARRET ICON}`}
          </div> */}

          {React.cloneElement(this.props.children[0], {
            className: `${this.props.children[0].props.className} accordion__section-title`
          })} 
        </AccordionSectionHeader>
        <div 
        className={`accordion__section-content ${openClassName}`}>
          <div 
          className="accordion__section-inner" 
          ref={ element => this.ref_AccordionSectionInner = element }>
            {this.props.children[1]}
          </div>
        </div>
      </div>
    )
  }
}

export default AccordionSection;


export const AccordionSectionHeader = props => {
  return (
    <div
      className={`accordion__section-header ${props.openClassName}`}
      {...props}>
      {props.children}
    </div>
  )
}

AccordionSection.propTypes = {
  /**
   * 
   * 
   * @param {String} label the section label
   */
  onClick: PropTypes.func.isRequired,

  /** Will render the first two children,
   * child one will be the header,
   * child two will be the content. 
  */
  children: PropTypes.element.isRequired,
}