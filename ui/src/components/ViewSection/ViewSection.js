import React from 'react';
import './ViewSection.scss';
import PropTypes from 'prop-types';

let ViewSection = (props) => {
  return (
    <section className="view-section">
      { props.title ?  <h2  className="view-section__title">{props.title}</h2> : null }
      <div className="view-section__content">
        {props.children}
      </div>
    </section>
  );
};

ViewSection.propTypes = {
  children: PropTypes.any,
  updateModelAttributes: PropTypes.func,
}

export default ViewSection;