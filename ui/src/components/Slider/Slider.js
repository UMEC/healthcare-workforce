import React from 'react';
import './Slider.scss';
import './Slider.css';

let Slider = (props) => {
  return (
    <div className="slidecontainer">
      <input type="range" className="slider" id={props.id} min={props.min} max={props.max} defaultValue={props.default} step={props.step}/>
    </div>
  );
};

export default Slider;