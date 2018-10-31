import { SET_MODEL_GEO_FILTER } from '../actions';

let defaultFilterState = {

  activeFilters: {
    geo: {
      area: 'State of Utah',
      sdoh_index: 3,
      availableProviders: [
        'Physician',
      'Physicial Assistant',
      'Nurse Practitioner',
      'Registered Nurse',
      'Doctor of Pharmacy',
      'Medical Assistant',
      'Educator',
      'Psychiatrist',
      'Licensed Clinical Social Worker',
      'Certified Mental Health Counselor',
      'Marriage and Family Therapists'
      ],
    geo_provider_types: {
      Phys: {
        provider_name: 'Physician',
          provider_abbr: 'Phys'
      },
      PA: {
        provider_name: 'Physicial Assistant',
          provider_abbr: 'PA'
      },
      NP: {
        provider_name: 'Nurse Practitioner',
          provider_abbr: 'NP'
      },
      RN: {
        provider_name: 'Registered Nurse',
          provider_abbr: 'RN'
      },
      PharmD: {
        provider_name: 'Doctor of Pharmacy',
          provider_abbr: 'PharmD'
      },
      MA: {
        provider_name: 'Medical Assistant',
          provider_abbr: 'MA'
      },
      Educ: {
        provider_name: 'Educator',
          provider_abbr: 'Educ'
      },
      Psych: {
        provider_name: 'Psychiatrist',
          provider_abbr: 'Psych'
      },
      LCSW: {
        provider_name: 'Licensed Clinical Social Worker',
          provider_abbr: 'LCSW'
      },
      CMHC: {
        provider_name: 'Certified Mental Health Counselor',
          provider_abbr: 'CMHC'
      },
      MFT: {
        provider_name: 'Marriage and Family Therapists',
          provider_abbr: 'MFT'
      }
    },
    provider_supply: [
      {
        provider_num: 502,
        provider_growth_trend: 0.01,
        provider_mean_wage: 177958,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 274,
        provider_growth_trend: 0.01,
        provider_mean_wage: 105690,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 602,
        provider_growth_trend: 0.01,
        provider_mean_wage: 95994,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 2145,
        provider_growth_trend: 0.01,
        provider_mean_wage: 57595,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 1102,
        provider_growth_trend: 0.01,
        provider_mean_wage: 125000,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 943,
        provider_growth_trend: 0.01,
        provider_mean_wage: 32500,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 1093,
        provider_growth_trend: 0.01,
        provider_mean_wage: 55652,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 441,
        provider_growth_trend: 0.01,
        provider_mean_wage: 204194,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 1093,
        provider_growth_trend: 0.01,
        provider_mean_wage: 62000,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 391,
        provider_growth_trend: 0.01,
        provider_mean_wage: 52500,
        provider_wage_trend: 0.02
      },
      {
        provider_num: 270,
        provider_growth_trend: 0.01,
        provider_mean_wage: 55590,
        provider_wage_trend: 0.02
      }
    ]
    }
  }
}
export default (state = defaultFilterState, action) => {
  switch (action.type) {
    case SET_MODEL_GEO_FILTER:
      state.activeFilters = { ...state.activeFilters, ...action.payload};
      return {...state};
    default:
      return {...state};
  }
}