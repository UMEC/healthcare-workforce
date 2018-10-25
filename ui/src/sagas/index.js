import {
  GET_ANALYTICS_IDS_REQUEST,
  GET_ANALYTICS_IDS_SUCCESS,
  GET_ANALYTICS_IDS_FAILURE,
} from '../actions';

import { all, call, put, takeLatest } from 'redux-saga/effects';
// import axios from 'axios';

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

const callAnalyticsPostApi = async () => {
  const response = await fetch('/api/analytics', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ "params": { "type": "cost_quality_adjustment", "value": 0.5 } })
  });

  const body = await response.json();

  if (response.status !== 200) throw Error(body.message);
  console.log("Post respnse: " + JSON.stringify(body));
  return body;
};

const callAnalyticsGetApi = async (modelId) => {
  const response = await fetch('/api/analytics/' + modelId, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
  });

  const body = await response.json();

  if (response.status !== 200) throw Error(body.message);
  console.log("Get response: " + JSON.stringify(body));
  return body;
};

function* requestAnalyticsIDs() {
  try {
    const defaultModelData = yield call(callAnalyticsPostApi);
    // const body = yield response;
    // const modelId = yield callAnalyticsGetApi(body.modelId);

    const payload = {
      defaultModelData,
    };

    yield put({ type: GET_ANALYTICS_IDS_SUCCESS, payload });
  } catch (error) {
    yield put({ type: GET_ANALYTICS_IDS_FAILURE, error });
  }
}

function* requestAnalyticsWatcher() {
  yield takeLatest(GET_ANALYTICS_IDS_REQUEST, requestAnalyticsIDs);
}

function* rootSaga() {
  yield all([
    requestAnalyticsWatcher(),
  ])
}

export default rootSaga;