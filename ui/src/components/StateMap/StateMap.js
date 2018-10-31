import React from 'react';
import './StateMap.scss';
import { SVGMap } from 'react-svg-map';
import Utah from './utah';
import CheckboxUtahMap from './checkbox-utah-map';


let StateMap = (props) => {
  return (
    //<SVGMap map={Utah} />
    <CheckboxUtahMap/>
  );
};

export default StateMap;