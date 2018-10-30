import React, { Component } from 'react';
import _ from 'lodash';

class Panel extends Component {
  constructor(props) {
    super(props);

    this.handleGeoFilterChange = this.handleGeoFilterChange.bind(this);
  }

  scrambleString = (string) => {
    let newString = _.camelCase(string);
    let stringArray = newString.split('');
    let scrambledArray = _.shuffle(stringArray);
    let scrambledString = scrambledArray.join('');
    return scrambledString;
  }

  handleGeoFilterChange(e) {
    let newGeoFilter = { geo: this.props.modelFilters.allFilters.geos[e.target.value] };
    this.props.handleGeoFilterUpdate(newGeoFilter);
  }

  render() {
    return (
      <aside className="panel">
        <select 
          value={this.props.modelFilters.activeFilters.geo.area}
          onChange={this.handleGeoFilterChange}>
          {_.map(this.props.modelFilters.allFilters.geos, geo => {
            return (
              <option
                key={this.scrambleString(geo.area)}
              value={geo.area}>
              {geo.area}
              </option>
            );
          })}
        </select>
      </aside>
    );
  }

};

export default Panel;