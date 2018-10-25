import React from 'react';
import './ViewContainer.scss';

let ViewContainer = (props) => {
  return (
    <main className="view-container">
      {props.children}
    </main>
  );
};

export default ViewContainer;