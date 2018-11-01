import {staticGeoProfileResponse} from './static-json-responses';

let raw_providers = [
  {
    "provider_name": "Physician",
    "provider_abbr": "Phys"
  },
  {
    "provider_name": "Physicial Assistant",
    "provider_abbr": "PA"
  },
  {
    "provider_name": "Nurse Practitioner",
    "provider_abbr": "NP"
  },
  {
    "provider_name": "Registered Nurse",
    "provider_abbr": "RN"
  },
  {
    "provider_name": "Psychiatrist",
    "provider_abbr": "Psych"
  },
  {
    "provider_name": "Licensed Clinical Social Worker",
    "provider_abbr": "LCSW"
  },
  {
    "provider_name": "Certified Mental Health Counselor",
    "provider_abbr": "CMHC"
  },
  {
    "provider_name": "Marriage and Family Therapists",
    "provider_abbr": "MFT"
  },
  {
    "provider_name": "Doctor of Pharmacy",
    "provider_abbr": "PharmD"
  },
  {
    "provider_name": "Medical Assistant",
    "provider_abbr": "MA"
  },
  {
    "provider_name": "Educator",
    "provider_abbr": "Educ"
  }
]

let geoProfile = Object.values(staticGeoProfileResponse).reduce((previous, item, index, array) => {
  let all_geo_names = Object.keys(staticGeoProfileResponse);
  let providers = raw_providers.reduce((previous, next) => {
    return { ...previous, [next.provider_abbr]: next }
  }, {});

  let geo_name = all_geo_names[index];


  let geo_provider_types = Object.keys(item.supply);

  let foo = geo_provider_types
    .reduce((previous, item) => {
      let provider_attrs = providers[item];
      let next = { ...previous, [item]: provider_attrs };
      return next;
    }, {});
    
  let bar = geo_provider_types
    .reduce((previous, item) => {
      let provider_attrs = providers[item];
      let next = [...previous, provider_attrs.provider_name ];
      return next;
    }, []);

  let provider_supply = Object.values(item.supply)
    .reduce((previous, item) => {
      let provider_abbr = geo_provider_types[index];
      let provider_name = providers[provider_abbr];
      
      let provider_info = {
        provider_abbr,
        provider_name,
        ...item
      }

      return [...previous, provider_info]
    }, []);

  let geo_profile = {[geo_name]: {
    area: geo_name,
    sdoh_index: item.sdoh_index,
    availableProviders: bar,
    geo_provider_types: foo,
    provider_supply,
  }}

  let next = {...previous, ...geo_profile}
  return next;
}, {})


export default (state = geoProfile, action) => {
  switch (action.type) {
    case 'value':
      return state;
      break;
  
    default:
      return state;
      break;
  }
}