import activeModelDefaultState from './mock-default-state';
import _ from 'lodash';
import {
  MODEL_REQUEST,
  MODEL_SUCCESS,
  MODEL_FAILURE,
} from '../actions';
// import { actionChannel } from 'redux-saga/effects';

// reshaping default state to next the 
const modelOutput = {
  servicesByProvider: activeModelDefaultState
};
// const supply = _.mapValues(_.groupBy(activeModelDefaultState.response.supply, 'provider_county'));
// const services = _.mapValues(_.groupBy(activeModelDefaultState.response.services, 'acute_encounter'));

// debugger;

export default (state = modelOutput, action) => {
  switch (action.type) {
    case MODEL_REQUEST:
      return { loading: true, error: null };
    // case MODEL_SUCCESS:
    //   return action.payload;
    // case MODEL_FAILURE:
    //   return action.payload;
    default:
      return state;
  }
}