import { SET_MODEL_GEO_FILTER } from '../actions';

let defaultFilterState = {

  activeFilters: {
    geo: {area: 'all', availableProviders: [] },
    providerType: {},
  },
  allFilters: {
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
export default (state = defaultFilterState, action) => {
  switch (action.type) {
    case SET_MODEL_GEO_FILTER:
      state.activeFilters = { ...state.activeFilters, ...action.payload};
      return {...state};
    default:
      return {...state};
  }
}