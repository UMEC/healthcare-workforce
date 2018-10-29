import React from 'react';
import './ViewFooter.scss';
import PropTypes from 'prop-types';

let ViewFooter = (props) => {
  return (
    <footer className="view-footer">
      {props.children}
    </footer>
  );
};

ViewFooter.propTypes = {
  children: PropTypes.any
}

export default ViewFooter;