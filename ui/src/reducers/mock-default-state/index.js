let activeModel = require('./providers');

const STRING = JSON.stringify(activeModel);
const activeModelDefaultState = JSON.parse(STRING);

export default  activeModelDefaultState;