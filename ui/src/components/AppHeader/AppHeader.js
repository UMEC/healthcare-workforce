import React from 'react';
import './AppHeader.scss';

let AppHeader = (props) => {
  return (
    <header className="app-header">
      {props.children}
    </header>
  );
};

export default AppHeader;