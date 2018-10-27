import React from 'react';
import './AppContent.scss';

let AppContent = (props) => {
  return (
    <div className="app-content">
      {props.children}
    </div>
  );
};

export default AppContent;