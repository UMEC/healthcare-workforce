import React, { Component } from 'react';
import PropTypes from 'prop-types';
import _ from 'lodash';
import map from 'lodash/map';
// import { bindActionCreators } from 'redux';

// import { connect } from 'react-redux';

class ProviderRoles extends Component {
  constructor(props) {
    super(props);
    this.state = {
      addedProviderTypes: ['Physicial Assistant'],
      defaultServicesByProvider: this.reshapeNewServicesByProvider(),
      customServicesByProvider: this.reshapeNewServicesByProvider(),
    };
  }

  reshapeNewServicesByProvider = () => {
    let { servicesByProvider } = this.props;

    // TODO: This is temporary
    // It's a temporary fix to get the data in a easily consumable format 
    // so it can be easily iterated over. Whether or not it's going to work 
    // on with the pythin API model output... TBD.
    // - Dom W
    let transformedServicesByProvider = map(servicesByProvider, provider => {
      // let providerAbbr = Object.getOwnPropertyName(provider);
      let providerType = provider.provider_type;
      // create a list of service categories using keys of the provider services 
      // array (which corespond to the service category) to be used when creating 
      // the service category object.
      let service_categories = provider['services:'].reduce((prev, item) => { return [...prev, Object.keys(item)[0]] }, [])

      // Create a `service_categories` array containing category objects that 
      // describe the category and all services within it.
      let services = _.reduce(provider['services:'], (previous, item, index) => {
        // Use the index of the current service to get it's `service_category`
        // from the array of `service_categories.
        let service_category = service_categories[index];
      
        let services = _.reduce(item, (previous, service) => {

          let services = Object.values(service)
            .map(item => item)
            .reduce((previous, service) => {
              let service_name = Object.getOwnPropertyNames(service)[0];
              let service_info = Object.values(service)[0];

              let service_attrs = {
                service_name,
                service_info,
              }
              return previous = [...previous, service_attrs];
            }, []);

          let serviceObj = {
            service_category,
            services,
          }

          return previous = [...previous, serviceObj];
        }, [])
        return [...previous, services]
      }, [])


      let newProviderServices = {
        // provider_abbr: providerAbbr,
        provider_type: providerType,
        provider_services: services,
      };
      return newProviderServices;
    });
    return transformedServicesByProvider;
  }

  filteredServicesByProvider = () => {
    let { availableProviders } = this.props.activeFilters.geo;
    let { addedProviderTypes } = this.state;

    if (availableProviders.length === 0 ) return this.state.customServicesByProvider;

    let providersList = [...availableProviders, ...addedProviderTypes]


    let foo = providersList.reduce( (previous, provider) => {
      let current = this.state.customServicesByProvider.filter(item => {

        return provider === item.provider_type;
      });
      let next = [...previous, current[0]]
      return next;
      }, [])
      // get only the providers available in a specific area 
      // 
      return foo;
  }

  updateScoreValue = (services, index, e) => {
    let currentServiceAttrs = services[index];

    currentServiceAttrs.service_info.score = Number.parseFloat(e.target.value).toFixed(2);

    this.props.updateModelAttributes(currentServiceAttrs)
  }

  sliderColor = (usagePercentage) => {
    if (usagePercentage >= 80) {
      return '#b30000';
    } else if (usagePercentage > 75){
      return '#e68200';
    } else if (usagePercentage <= 10){
      return '#0c3f68';
    } else {
      return '#308715';
    }
  }

  // helpful for scrabmling strings for unique keys when mapping
  scrambleString = (string) => {
    let newString = _.camelCase(string);
    let stringArray = newString.split('');
    let scrambledArray = _.shuffle(stringArray);
    let scrambledString = scrambledArray.join('');
    return scrambledString;
  }
  
  renderServices = (services, providerObject) => {
    return services.map((service, index) => {
      let serviceScore = providerObject.provider_services;
      
      let usagePercentage = Number.parseFloat(service.service_info.score * 100).toFixed(0);
      let sliderColor = this.sliderColor(usagePercentage);

      return (
        <div
          key={this.scrambleString(`${service.service_name}${usagePercentage}${index}`)}
          className="provider-roles__service-attributes" >
          <p className="provider-roles__service-label">
            {service.service_name}
          </p>
          <p>BOL/TOL: <span style={{color: sliderColor}}>{usagePercentage}%</span></p>
          <input 
            type="range" 
            min="0" 
            max="1" 
            value={service.service_info.score}
            step="0.01" 
            className="slider"
            onChange={(e) => this.updateScoreValue(services, index, e)}></input>
          <p>Face To Face time</p>
          <p>min: {service.service_info.min_f2f_time}</p>
          <p>max: {service.service_info.max_f2f_time}</p>
        </div>
    )})
  }

  renderServiceCategories = (categories, providerObject) => {
      return categories.map(providerServices => {
        return (
          <div 
            key={this.scrambleString(providerServices[0].service_category)}
            className="provider-roles__category">
            <p
              className="provider-roles__category-header">
              {providerServices[0].service_category}
            </p>
            <div className="provider-roles__category-body">
              {this.renderServices(providerServices[0].services, providerObject)}
            </div>
          </div>
        )
      })
  }

  renderProviders = (providers) => {

    
    
    return providers.map(provider => {
      return (
        <>
          <div key={this.scrambleString(provider.provider_type)} className="accordion__header">
            <p 
              className="provider-roles__section-title"
              onClick={() => this.props.updateModelAttributes(provider.provider_type, provider)}>{provider.provider_type}
            </p>
          </div>
          <div key={this.scrambleString(provider.provider_type)} className="accordion__content">
            {this.renderServiceCategories(provider.provider_services, provider)}
          </div>
        </>
      );

    })
  }

  render() {
    const { area } = this.props.activeFilters.geo;

    const filteredProviders = this.filteredServicesByProvider()

    let titleString = area !== 'all' 
      ? `ProviderRoles for ${area}`
      : `All Providers`;
    return (
      <>
        <p>{titleString}</p>
        <div className="accordion">

          {this.renderProviders(filteredProviders)}
        </div>
      </>
    );
  }
}

ProviderRoles.protoTypes = {
  servicesByProvider: PropTypes.object,
  /**
   * addedProviderTypes: Array of pro
   */
  addedProviderTypes:  PropTypes.arrayOf(
    
  )
}

// function mapStateToProps(state) {
//   return {
//     defaultModel: state.defaultModel,
//   }
// }

export default ProviderRoles;