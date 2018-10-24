
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
app.use('/api/source', require("./api/source"))
app.use('/api/analytics', require("./api/analytics"))
app.use('/api/user', require("./api/user"))

app.listen(process.env.PORT || 3000)