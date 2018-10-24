const DIR_ANALYTICS_FILES = "C:/workdir/analytics/";
let router = require('express').Router();
var fs = require('fs');
var ps = require('python-shell');

const bodyParser = require('body-parser');
router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json())

/* Retrieve the list of known analytics model requests. */
router.get('/', (req, res) => {
    initUserSession(req);
    
    var allRequests = [];
    Object.keys(req.session.user.analytics).forEach(function(key) {
        var item = Object.assign({}, req.session.user.analytics[key]);
        // interested in everything except the actual data
        item.data = undefined;
        allRequests.push(item);
    });

    res.writeHead(200, {'Content-Type': 'application/json'});
    res.write(JSON.stringify(allRequests));
    return res.end();
});

/* Create a new analytic model request. */
router.post('/', (req, res) => {
    initUserSession(req);

    var uuid = require('uuid-random');
    var modelRequest = {
        "modelId": uuid(),
        "status" : "new",
        "request_date": new Date(),
        "params": req.body.params
    };
    
    req.session.user.analytics.push(modelRequest);
    
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.write(JSON.stringify(modelRequest));
    res.end();

    console.log("Constructing promise!");
    Promise.resolve()
      .then(function(){
        return invokeModelRequest(req, modelRequest.modelId, modelRequest.params);
      });
    console.log("Finished constructing promise!"); 
});

/* Get an existing analytic model request. */
router.get('/:modelId', (req, res) => {
    initUserSession(req);

    var modelId = req.params.modelId;
    var modelRequest = getModelRequest(req, modelId);

    if (!modelRequest) {
        res.status(404);
        res.send('Unknown modelId');
        res.end();
        return;
    }

    res.writeHead(200, {'Content-Type': 'application/json'});
    res.write(JSON.stringify(modelRequest));
    res.end();
});

/* Update an existing analytic model request. */
router.put('/:modelId', (req, res) => {
    initUserSession(req);

    var params = req.body.params;
    var modelId = req.params.modelId;
    var modelRequest = getModelRequest(req, modelId);
    if (!modelRequest) {
        res.status(404);
        res.send('Unknown modelId');
        res.end();
        return;
    }

    updateModelRequestWithNewRequest(req, modelId, "new", params);

    modelRequest = getModelRequest(req, modelId);
    
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.write(JSON.stringify(modelRequest));
    res.end();

    Promise.resolve()
      .then(function(){
        return invokeModelRequest(req, modelId, params);
      });
});

/* Persist an existing analytic model request against the current user. Must have a current user context. */
router.post('/:modelId/persist', (req, res) => {
    // invoke picklet persist?
    res.send('Not implemented');
    res.end();
});

function getModelRequest(req, id) {
    for (let key of Object.keys(req.session.user.analytics)) {
        if (req.session.user.analytics[key].modelId === id) {
            return req.session.user.analytics[key];
        }
    }

    return null;
}

function updateModelRequestWithResponse(req, modelId, newStatus, data) {
    req.session.reload(function(err) {
        // session updated
        for (let key of Object.keys(req.session.user.analytics)) {
            var thisItem = req.session.user.analytics[key];
            if (thisItem.modelId === modelId) {
                thisItem.status = newStatus;
                thisItem.data = data;
                req.session.user.analytics[key] = thisItem;
                req.session.save();
                console.log("Received model response for: " + key + " modelId " + req.session.user.analytics[key].modelId + " with status " + newStatus);
                return;
            }
        }
    })        
}

function updateModelRequestWithNewRequest(req, modelId, newStatus, params) {
    for (let key of Object.keys(req.session.user.analytics)) {
        var thisItem = req.session.user.analytics[key];
        if (thisItem.modelId === modelId) {
            thisItem.request_date = new Date();
            thisItem.status = newStatus;
            thisItem.data = [];
            if (!thisItem.historical_params) {
                thisItem.historical_params = [];
            }
            thisItem.historical_params.push(thisItem.params);
            thisItem.params = params;
            req.session.user.analytics[key] = thisItem;
            req.session.save();
            console.log("Updated model request for: " + key + " modelId " + req.session.user.analytics[key].modelId + " with status " + newStatus);
            return;
        }
    }
}

function invokeModelRequest(req, modelId, params) {
    console.log("Invoking model request for modelId: " + modelId + " with params: " + JSON.stringify(params));
    var options = {
        mode: 'text',
        args: [JSON.stringify(params)]
    };

    ps.PythonShell.run('../../models/gateway/analyticmodel.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        // console.log('Model response: %j', results);
        updateModelRequestWithResponse(req, modelId, "completed", results);
    }); 
}

function initUserSession(req) {
    if (!req.session.user) {
        console.log("Creating user session..");
        req.session.user = {};
    }

    if (!req.session.user.analytics) {
        console.log("Creating analytics session..");
        req.session.user.analytics = [];
    }
}

module.exports = router;