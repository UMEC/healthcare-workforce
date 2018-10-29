import { combineReducers } from 'redux';
import defaultModelReducer from './reducer-default-model';
import modelReducer from './reducer-model';

const rootReducer = combineReducers({
  defaultModel: defaultModelReducer,
  currentModelOutput: modelReducer,
});

export default rootReducer;