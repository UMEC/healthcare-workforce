import React, {Component} from 'react';
import _ from 'lodash';


class AccordionSection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      containerHeight: 0,
    }

    // this.handleAccordionToggle = this.handleAccordionToggle.bind(this);
  }

  componentDidMount() {
    this.handleAccordionHeightChange()
  }
  
  componentWillReceiveProps(nextProps) {
    
  }


  componentWillUnmount() {
  }
  
  handleAccordionToggle = (e) => {
    // console.log(this.ref_AccordionSectionInner.clientHeight)
    // this.handleAccordionHeightChange()
  }

  handleAccordionHeightChange = () => {
    // let combinedHeightOfChildren = Object.values(this.ref_AccordionSectionInner.querySelectorAll('.provider-roles__category'))
    //   .reduce((previous, item) => { 
    //     var marginTop = parseInt(item.style.marginTop) || 0;
    //     var marginBottom = parseInt(item.style.marginBottom) || 0;
    //     let verticalMargin = marginTop + marginBottom;

    //     return item.offsetHeight + verticalMargin + previous 
    //   }, 0)

    // console.log(combinedHeightOfChildren)

  }

  handleLabelClick = () => {
    this.handleAccordionHeightChange()
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