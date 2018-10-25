import { createStore, compose } from 'redux';
import { syncHistoryWithStore } from 'react-router-redux';
import browserHistory from './history';

// Import root reducer 
import rootReducer from './reducers';

const defaultState = {};

const store = createStore(rootReducer, defaultState);

export const history = syncHistoryWithStore(browserHistory, store);

export default store;