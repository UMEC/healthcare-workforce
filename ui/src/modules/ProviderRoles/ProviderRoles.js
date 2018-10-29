import React, { Component } from 'react';
import PropTypes from 'prop-types';
import _ from 'lodash';
import map from 'lodash/map';
import values from 'lodash/values';
import keys from 'lodash/keys';
// import { bindActionCreators } from 'redux';

// import { connect } from 'react-redux';

class ProviderRoles extends Component {
  constructor(props) {
    super(props);
    this.state = {
      availableProviderTypes: this.props.availableProviderTypes,
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

      let services = _.reduce(provider['services:'], (previous, item) => {

        let services = _.reduce(item, (previous, service) => {
          let service_category = Object.values(service)
            .reduce((previous, item) => {
              let service_category = Object.getOwnPropertyNames(item)[0];
              return service_category
            }, '');

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
    let { availableProviderTypes, addedProviderTypes } = this.state;
    let providersList = [...availableProviderTypes, ...addedProviderTypes]

    if (!availableProviderTypes) return this.state.customServicesByProvider

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

  createPath = (obj, path, value = null) => {
    path = typeof path === 'string' ? path.split('.') : path;
    let current = obj;
    while (path.length > 1) {
      const [head, ...tail] = path;
      path = tail;
      if (current[head] === undefined) {
        current[head] = {};
      }
      current = current[head];
    }
    current[path[0]] = value;
    return obj;
  };

  updateScoreValue = (services, index) => {
    let currentServiceAttrs = services[index];
    console.log(typeof currentServiceAttrs.service_info.score)
    currentServiceAttrs.service_info.score = Math.abs(currentServiceAttrs.service_info.score )+ 0.1;

    this.props.updateModelAttributes(currentServiceAttrs)
    _.debounce(() =>{

    }, 100)
  }

  renderServices = (services) => {
    return services.map((service, index) => {


      // 

      return (
        <div
          className="provider-roles__service-attributes"
          onClick={() => this.updateScoreValue(services, index)} >
          <p className="provider-roles__service-label">
            {service.service_name}</p>
          <p>Score: {service.service_info.score}</p>
          <input type="range" min="0" max="1" value={service.service_info.score} step="0.01" class="slider" id="myRange"></input>
          <p>Face To Face time</p>
          <p>min: {service.service_info.min_f2f_time}</p>
          <p>max: {service.service_info.max_f2f_time}</p>
        </div>
    )})
  }

  renderServiceCategories = (categories, providerObject) => {
    // let categoriesObject = this.createPath(providersObject, 'providerServices[0].service_category', 1 )
    // console.log(providerObject);
      return categories.map(providerServices => {
        return (
          <>
            <p
              className="provider-roles__section-category">
              {providerServices[0].service_category}
            </p>
            {this.renderServices(providerServices[0].services, providerServices[0].services)}
          </>
        )
      })
  }

  renderProviders = (providers) => {
    let providersObject = this.createPath({}, 'provider_type', 1);

    
    
    return providers.map(provider => {
      // providersObject.provider_type = provider;
      // console.log(provider)
      return (
        <>
          <div className="accordion__header">
            <p 
              className="provider-roles__section-title"
              onClick={() => this.props.updateModelAttributes(provider.provider_type, providersObject)}>{provider.provider_type}
            </p>
          </div>
          <div className="accordion__content">
            {this.renderServiceCategories(provider.provider_services, provider)}
          </div>
        </>
      );

    })
  }

  render() {
    const { customServicesByProvider } = this.state;
    this.filteredServicesByProvider()

    const filteredProviders = this.filteredServicesByProvider()

    return (
      <>
        <p>ProviderRoles</p>
        <div className="accordion">

          {this.renderProviders(filteredProviders)}
        </div>
      </>
    );
  }
}

ProviderRoles.protoTypes = {
  servicesByProvider: PropTypes.object
}

// function mapStateToProps(state) {
//   return {
//     defaultModel: state.defaultModel,
//   }
// }

export default ProviderRoles;