import {
  MODEL_REQUEST,
  MODEL_SUCCESS,
  MODEL_FAILURE,
} from '../actions';
// import { actionChannel } from 'redux-saga/effects';

const initialState = {};

export default (state = initialState, action) => {
  switch (action.type) {
    case MODEL_REQUEST:
      return { loading: true, error: null };
    case MODEL_SUCCESS:
      return action.payload;
    case MODEL_FAILURE:
      return action.payload;
    default:
      return state;
  }
}