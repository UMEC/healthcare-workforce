import { combineReducers } from 'redux';
import defaultModelReducer from './reducer-default-model';
import modelReducer from './reducer-model';
import modelFiltersReducer from './reducer-model-filters';

const rootReducer = combineReducers({
  defaultModel: defaultModelReducer,
  currentModelOutput: modelReducer,
  modelFilters: modelFiltersReducer,
});

export default rootReducer;