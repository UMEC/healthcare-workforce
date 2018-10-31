import React from 'react';
import './AppHeader.scss';

let AppHeader = (props) => {
  return (
    <header className="app-header">
      <div className="app-branding">
        <h1><abbr title="Utah Medical Education Council" >UMEC</abbr> Gap Analysis Tool</h1>
      </div>
      {props.children}
    </header>
  );
};

export default AppHeader;