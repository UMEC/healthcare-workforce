import React from 'react';
import './TeamComposition.scss';

let TeamComposition = (props) => {
  return (
    <div className="team-composition__wrapper">
      <div className="wrapper team-composition__header-row">
        <div className="box">Current</div>
        <div className="box">Role</div>
      </div>
        {props.supply.map(item => {
          return (
            <div className="wrapper">
              <div className="box">{item.provider_num}</div>
              <div className="box">{item.provider_name}</div>
            </div>
          )
        })}
    </div>
  );
};

export default TeamComposition;