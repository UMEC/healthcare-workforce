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
  // let {response2, error2} = yield call(getModelData, response.data.modelId);
  // debugger;

  
  if (response) {
    let { modelId } = response.data;

    yield put({ type: MODEL_INFO_SUCCESS, payload: { ...response.data} })
    yield put({ type: MODEL_REQUEST, modelId })
    
  } else {
    yield put({ type: MODEL_INFO_FAILURE, error })
  } 
  // let foo = yield call()
  
}

function* requestModel(modelId) {
  let { response, error } = yield call(getModelData, modelId);

  if (response) {
    yield put({ type: MODEL_SUCCESS, payload: response.data })
  } else {
    yield put({ type: MODEL_FAILURE, payload: error })
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