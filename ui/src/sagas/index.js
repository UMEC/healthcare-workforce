import {
  INITIAL_MODEL_INFO_REQUEST,
  MODEL_INFO_REQUEST,
  MODEL_INFO_SUCCESS,
  MODEL_INFO_FAILURE,
} from '../actions';

import { all, call, put, takeLatest } from 'redux-saga/effects';
import axios from 'axios';

// function* postAnalytics() {
//   const response = fetch('/api/analytics', {
//     method: 'POST',
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ "params": { "type": "cost_quality_adjustment", "value": 0.5 } })
//   });

//   // if (response.status !== 200) throw Error(body.message);
//   // console.log("Post respnse: " + JSON.stringify(body));
//   return response.json();
// };

// function* callAnalyticsGetApi(modelId) {
//   const response = fetch('/api/analytics/' + modelId, {
//     method: 'GET',
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json',
//     }
//   });

//   // if (response.status !== 200) throw Error(body.message);
//   // console.log("Get response: " + JSON.stringify(body));
//   return response.json();
// };

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

// const callAnalyticsGetApi = async (modelId) => {
//   const response = await fetch('/api/analytics/' + modelId, {
//     method: 'GET',
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json',
//     }
//   });

//   const body = await response.json();

//   if (response.status !== 200) throw Error(body.message);
//   console.log("Get response: " + JSON.stringify(body));
//   return body;
// };

function* requestModelInfo(modelParams) {
  let { response, error } = yield call(getModelInfo, modelParams);
  // const body = yield response;
  
  if (response) {

    let modelData = yield getModelData(response.data.modelId);

    yield put({ type: MODEL_INFO_SUCCESS, payload: {...response.data, ...modelData.data} })
  } else {
    yield put({ type: MODEL_INFO_FAILURE, error })
  } 
}

function* requestModelInfoWatcher(modelParams) {
  yield takeLatest(MODEL_INFO_REQUEST, requestModelInfo, modelParams);
}

function* requestInitialModelInfoWatcher(modelParams = defaultModelParams) {
  if (localStorage.getItem('state')) return;
  yield takeLatest(INITIAL_MODEL_INFO_REQUEST, requestModelInfo, modelParams);
}

function* rootSaga() {
  yield all([
    requestModelInfoWatcher(),
    requestInitialModelInfoWatcher(),
  ])
}

export default rootSaga;