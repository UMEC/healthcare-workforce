import { combineReducers } from 'redux';
import defaultModelReducer from './reducer-default-model';
import modelReducer from './reducer-model';
import modelFiltersReducer from './reducer-model-filters';
import geoProfilesReducer from './reducer-geo-profiles';

const rootReducer = combineReducers({
  defaultModel: defaultModelReducer,
  currentModelOutput: modelReducer,
  modelFilters: modelFiltersReducer,
  geoProfile: geoProfilesReducer,
});

export default rootReducer;