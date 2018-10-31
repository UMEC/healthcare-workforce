let activeModel = require('./providers');
let geoProfileResponse = require('./geoProfiles');


function convertToObject( json ) {
  logger( json )
  const JSONstring = JSON.stringify(json);
  logger( JSONstring )
  const parsedJSON = JSON.parse(JSONstring);
  logger( parsedJSON )
  return parsedJSON;
}

function logger(input) {
  console.log(`typeof: ${typeof input}`, input )
}

// const activeModelDefaultState = convertToObject(activeModel);
const activeModelDefaultState = activeModel;
const staticGeoProfileResponse = geoProfileResponse.data.response;

export default  activeModelDefaultState;

export {
  activeModelDefaultState,
  staticGeoProfileResponse,
};