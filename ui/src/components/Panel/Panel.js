import React, { Component } from 'react';
import _ from 'lodash';

class Panel extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modelFilters: {
        geo: { area: 'all', availableProviders: [] },
        providerType: {},
      },
      filters: {
        geos: {
          'all': { area: 'all', availableProviders: [] },
          'county a': { area: 'county a', availableProviders: ["Physician", "Psychiatrist", "Doctor of Pharmacy", "Educator"] },
          'county b': { area: 'county b', availableProviders: ["Physician", "Medical Assistant"] },
        },
        providerTypes: {
          'Phys': { 'provider_name': 'Physician', 'provider_abbr': 'Phys' }, 
          'PA': { 'provider_name': 'Physicial Assistant', 'provider_abbr': 'PA' }, 
          'NP': { 'provider_name': 'Nurse Practitioner', 'provider_abbr': 'NP' }, 
          'RN': { 'provider_name': 'Registered Nurse', 'provider_abbr': 'RN' }, 
          'Psych': { 'provider_name': 'Psychiatrist', 'provider_abbr': 'Psych' }, 
          'LCSW': { 'provider_name': 'Licensed Clinical Social Worker', 'provider_abbr': 'LCSW' }, 
          'CMHC': { 'provider_name': 'Certified Mental Health Counselor', 'provider_abbr': 'CMHC' }, 
          'MFT': { 'provider_name': 'Marriage and Family Therapists', 'provider_abbr': 'MFT' }, 
          'PharmD': { 'provider_name': 'Doctor of Pharmacy', 'provider_abbr': 'PharmD' }, 
          'MA': { 'provider_name': 'Medical Assistant', 'provider_abbr': 'MA' }, 
          'Educ': { 'provider_name': 'Educator', 'provider_abbr': 'Educ' }
        },
        condition: [],
      }
    }

    this.handleGeoFilterChange = this.handleGeoFilterChange.bind(this);
  }

  componentDidMount(nextProps, nextState) {
    this.props.handleFilterUpdate(this.state.modelFilters)
    // console.log(nextState)
  }

  handleGeoFilterChange(e) {
    console.log(e.target.value)
    // { modelFilters: { geo: state.geos[e.target.value] } }
    let newFilter = { modelFilters: { geo: this.state.filters.geos[e.target.value] } }
    this.props.handleFilterUpdate(newFilter)
    this.setState(newFilter)
  }
  render() {
    return (
      <aside className="panel">
        <select 
          value={this.state.modelFilters.geo.area}
          onChange={this.handleGeoFilterChange}>
          {_.map(this.state.filters.geos, geo => {
            return (
              <option
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