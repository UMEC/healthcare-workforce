import {
  INITIAL_MODEL_INFO_REQUEST,
  MODEL_REQUEST,
  MODEL_SUCCESS,
  MODEL_FAILURE,
  MODEL_INFO_REQUEST,
  MODEL_INFO_SUCCESS,
  MODEL_INFO_FAILURE,
} from '../actions';

import { all, call, put, takeLatest } from 'redux-saga/effects';
import axios from 'axios';
import { loadStateFromSessionStorage } from '../loadState';

const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
};

const defaultModelParams = {
  params: {
    type: "cost_quality_adjustment", 
    value: 0.5,
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
    .then(response => ({ response }))
    .catch(error => ({ error }));
}
function* requestModelInfo(modelParams) {
  let { response, error } = yield call(getModelInfo, modelParams);

  if (response) {
    let { modelId } = response.data;

    yield put({ type: MODEL_INFO_SUCCESS, payload: { ...response.data} })
    yield put({ type: MODEL_REQUEST, modelId })
    
  } else {
    yield put({ type: MODEL_INFO_FAILURE, error })
  } 
}

function* requestModel(modelId) {
  let { response, error } = yield call(getModelData, modelId);

  if (response) {
    yield put({ type: MODEL_SUCCESS, payload: response.data })
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
  // // debugger;
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