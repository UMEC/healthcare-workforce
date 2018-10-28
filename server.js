var cluster = require('cluster');

if (cluster.isMaster && process.env.NODE_ENV !== 'unittest') {
  var cpuCount = require('os').cpus().length;

  // Create a worker for each CPU
  for (var i = 0; i < cpuCount && Object.keys(cluster.workers).length < cpuCount; i += 1) {
    cluster.fork();
  }

  cluster.on('exit', function (worker) {
    // Replace the dead worker
    cluster.fork();
  });

} else {
  const express = require('express');
  var app = express();
  var uuid = require('uuid-random');

  var sess = {
    genid: function(req) {
        return uuid() // use UUIDs for session IDs
    },
    secret: 'mousemonkey',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
  }
  if (app.get('env') === 'production') {
    app.set('trust proxy', 1) // trust first proxy
    sess.cookie.secure = true // serve secure cookies
  }
  var session = require('express-session')
  app.use(session(sess));


  // Use Api routes in the App
  app.use('/api/source', require("./server/api/source"))
  app.use('/api/analytics', require("./server/api/analytics"))
  app.use('/api/user', require("./server/api/user"))
  app.use('/api/request', require("./server/ui/request"))

  if (process.env.NODE_ENV !== 'unittest') {
    app.listen(process.env.PORT || 5000)
  }

  module.exports = app;
}
