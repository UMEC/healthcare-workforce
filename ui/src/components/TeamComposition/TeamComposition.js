import React from 'react';
import './TeamComposition.scss';

let TeamComposition = (props) => {
  return (
    <div>
      <div class="wrapper">
        <div class="box">Current</div>
        <div class="box">Role</div>
      </div>
        {props.supply.map(item => {
          return (
            <div class="wrapper">
              <div class="box">{item.provider_num}</div>
              <div class="box">{item.provider_name}</div>
            </div>
          )
        })}
    </div>
  );
};

export default TeamComposition;