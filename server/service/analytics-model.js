/*
 * An internal service that facilitates requests to the analytical model module.
 */
const ps = require('python-shell');

/* Logging method for this service. */
function log(requestType, msg) {
  console.log(`/service/analytics:${requestType}: ${msg}`);
}

this.invokeModelRequest = (params, callback) => {
  log('POST|PUT', `Invoking model request with params: ${JSON.stringify(params)}`);

  const pyshell = new ps.PythonShell('models/4.1.1 Model Manipulation/model_manip.py');

  // sends a message to the Python script via stdin
  pyshell.send(JSON.stringify(params));

  pyshell.on('message', (message) => {
    callback(undefined, JSON.parse(message));
  });

  // end the input stream and allow the process to exit
  pyshell.end((err, code, signal) => {
    if (err) {
      log('POST|PUT', `Received python error - exit code ${code}, signal ${signal}, error ${err}`);
      callback(err);
    }
  });
};

module.exports = this;
