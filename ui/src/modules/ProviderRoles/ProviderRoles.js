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
    this.state = {};
  }

  render() {
    let { servicesByProvider } = this.props;

    let newProviderServicesObject = map(servicesByProvider, provider => {
      // let providerAbbr = Object.getOwnPropertyName(provider);
      let providerType = provider.provider_type;

      let services = _.reduce( provider['services:'], (previous, item) => {

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
      console.log('newProviderServices', newProviderServices)
      return newProviderServices;
    })

    console.log('newProviderServicesObject', newProviderServicesObject);

    return (
      <>
        <p>ProviderRoles</p>
        {newProviderServicesObject.map( provider => {
          return (
          <>
            <p>{provider.provider_type}</p>
            {provider.provider_services.map( providerServices => {
              return (
              <>
                <p>CATEGORY: {providerServices[0].service_category}</p>
                {providerServices[0].services.map( service => {
                  return (
                    <>
                    <p>Service Name: {service.service_name}</p>
                    <p>Score: {service.service_info.score}</p>
                    <p>min face to face time: {service.service_info.min_f2f_time}</p>
                    <p>max face to face time: {service.service_info.max_f2f_time}</p>
                    </>
                  )
                })}
                
              </>
              )
            })}
          </>
          );

        })}
      </>
    );
  }
}

ProviderRoles.protoTypes = {
  rolesByProvider: PropTypes.object
}

// function mapStateToProps(state) {
//   return {
//     defaultModel: state.defaultModel,
//   }
// }

export default ProviderRoles;