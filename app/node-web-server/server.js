
const express = require('express');
var app = express();

// Use Api routes in the App
app.use('/api/source', require("./api/source"))
app.use('/api/analytics', require("./api/analytics"))
app.use('/api/user', require("./api/user"))

app.listen(process.env.PORT || 3000)