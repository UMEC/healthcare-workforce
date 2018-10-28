import {
  INITIAL_MODEL_INFO_REQUEST,
  MODEL_INFO_REQUEST,
  MODEL_INFO_SUCCESS,
  MODEL_INFO_FAILURE,
} from '../actions';
// import { actionChannel } from 'redux-saga/effects';

const initialState = {};

export default (state = initialState, action) => {
  switch (action.type) {
    case MODEL_INFO_REQUEST:
      return { ...state, fetchingAnalyticsIDs: true, error: null};
    case MODEL_INFO_SUCCESS:
      return { ...state, fetchingAnalyticsIDs: false, ...action.payload};
    case MODEL_INFO_FAILURE:
      return {...state, error: action.error};
    default:
      return state;
  }
}