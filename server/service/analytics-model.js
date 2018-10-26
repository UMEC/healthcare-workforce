const ps = require('python-shell');

this.invokeModelRequest = (params, callback) => {
  console.log(`Invoking model request with params: ${JSON.stringify(params)}`);

  const pyshell = new ps.PythonShell('models/4.1.1 Model Manipulation/model_manip.py');

  // sends a message to the Python script via stdin
  pyshell.send(JSON.stringify(params));

  pyshell.on('message', (message) => {
    callback(undefined, JSON.parse(message));
  });

  // end the input stream and allow the process to exit
  pyshell.end((err, code, signal) => {
    if (err) {
      console.log(`Received python error - exit code ${code}, signal ${signal}, error ${err}`);
      callback(err);
    }
  });
};

module.exports = this;
