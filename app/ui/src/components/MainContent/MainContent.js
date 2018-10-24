import React from 'react';
import './MainContent.scss';

let MainContent = (props) => {
  return (
    <main className="main-content">
      {props.children}
    </main>
  );
};

export default MainContent;