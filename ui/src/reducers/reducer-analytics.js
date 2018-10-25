import { 
  GET_ANALYTICS_IDS_REQUEST,
  GET_ANALYTICS_IDS_SUCCESS,
  GET_ANALYTICS_IDS_FAILURE,
} from '../actions';
// import { actionChannel } from 'redux-saga/effects';

const initialState = {
  analyticsIDs: null,
  fetchingAnalyticsIDs: false,
  error: null,
  defaultModelData: {},
};

export default (state = initialState, action) => {
  switch (action.type) {
    case GET_ANALYTICS_IDS_REQUEST:
      return { ...state, fetchingAnalyticsIDs: true, error: null};
    case GET_ANALYTICS_IDS_SUCCESS:
      return { ...state, fetchingAnalyticsIDs: false, defaultModelData: action.payload.defaultModelData };
    case GET_ANALYTICS_IDS_FAILURE:
      return {...state, error: action.error};
    default:
      return state;
  }
}