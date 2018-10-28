import {
  INITIAL_MODEL_INFO_REQUEST,
  MODEL_REQUEST,
  MODEL_SUCCESS,
  MODEL_FAILURE,
  MODEL_INFO_REQUEST,
  MODEL_INFO_SUCCESS,
  MODEL_INFO_FAILURE,
} from '../actions';

import { delay } from 'redux-saga';
import { all, call, put, fork, takeLatest } from 'redux-saga/effects';
import axios from 'axios';
import { loadStateFromSessionStorage } from '../loadState';

const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
};

const defaultModelParams = { 
  params: { 
    request_type: "provider_profile",
    value: "Psych",
  }
};

const getModelInfo = (modelParams) =>  {
  return axios.post('/api/analytics', modelParams, headers)
  .then( response => ({ response }))
  .catch( error => ({ error }))
}

const getModelData = (modelId) => {
  let route = `/api/analytics/${modelId}`;
  
  return axios.get(route, headers)
  .then( response => ({ response }))
  
  // .then(response =>{ 
  //   return response })
  .catch(error => ({ error }));

}
function* requestModelInfo(modelParams) {
  let { response, error } = yield call(getModelInfo, modelParams);

  if (response) {
    let { modelId } = response.data;
    
    yield put({ type: MODEL_INFO_SUCCESS, payload: response.data })
    // Get the model with the requestModel function
    yield call( requestModel, modelId );
    
  } else {
    yield put({ type: MODEL_INFO_FAILURE, error })
  } 
}

function* requestModel(modelId) {
  // TODO: Only call the model success if a status of completed is returned from 
  // `aoi/analytics/{modelId}`
  // a better way to do this would be to chech the status of the response with 
  // a set timeout function that periodically checks to see if this has completed 
  // on the model's end (in python) and when the status is complete, then when a 
  // satus of complete is returned -- use put() to add the data to state.
  yield call(delay, 1000)
  
  let { response, error } = yield call(getModelData, modelId);
  if (response) {
    yield put({ type: MODEL_SUCCESS, payload: response.data.data.response })
  } else {
    yield put({ type: MODEL_FAILURE, payload: error.response })
  }
}

function* requestModelInfoWatcher(modelParams) {
  yield takeLatest(MODEL_INFO_REQUEST, requestModelInfo, modelParams);
}

function* requestModelWatcher(modelId) {
  yield takeLatest(MODEL_REQUEST, requestModel, modelId);
}

function* requestInitialModelInfoWatcher(modelParams = defaultModelParams) {
  // let sessionState = yield loadStateFromSessionStorage();
  // if (sessionState.model.modelId) {
  //   console.log(`a modelId of ${sessionState.model.modelId} already exists in the session storage`);
  //   return
  // }
  yield takeLatest(INITIAL_MODEL_INFO_REQUEST, requestModelInfo, modelParams);

}

function* rootSaga() {
  yield all([
    requestModelInfoWatcher(),
    requestInitialModelInfoWatcher(),
    requestModelWatcher(),
  ])
}

export default rootSaga;