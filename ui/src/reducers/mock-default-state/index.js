let activeModel = require('./activeModelDefaultState');

const STRING = JSON.stringify(activeModel);
const activeModelDefaultState = JSON.parse(STRING);

export default  activeModelDefaultState;