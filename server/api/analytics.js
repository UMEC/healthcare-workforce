const router = require('express').Router();
const ps = require('python-shell');
const bodyParser = require('body-parser');
const uuid = require('uuid-random');

router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());

function initUserSession(req) {
  if (!req.session.user) {
    req.session.user = {};
  }

  if (!req.session.user.analytics) {
    req.session.user.analytics = [];
  }
}

function getModelRequest(req, id) {
  for (const key of Object.keys(req.session.user.analytics)) { // eslint-disable-line
    if (req.session.user.analytics[key].modelId === id) {
      return req.session.user.analytics[key];
    }
  }

  return null;
}

function updateModelRequestWithResponse(req, modelId, newStatus, data) {
  req.session.reload((err) => {
    if (err) throw err;
    // session updated
    for (let key of Object.keys(req.session.user.analytics)) { // eslint-disable-line
      const thisItem = req.session.user.analytics[key];
      if (thisItem.modelId === modelId) {
        thisItem.status = newStatus;
        thisItem.data = data;
        req.session.user.analytics[key] = thisItem;
        req.session.save();
        console.log(`Received model response for: ${req.session.user.analytics[key].modelId} with status ${newStatus}`);
        return;
      }
    }
  });
}

function updateModelRequestWithNewRequest(req, modelId, newStatus, params) {
  for (let key of Object.keys(req.session.user.analytics)) { // eslint-disable-line
    const thisItem = req.session.user.analytics[key];
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
      console.log(`Updated model request for:  ${req.session.user.analytics[key].modelId} with status ${newStatus}`);
      return;
    }
  }
}

function invokeModelRequest(req, modelId, params) {
  console.log(`Invoking model request for modelId: ${modelId} with params: ${JSON.stringify(params)}`);
  const options = {
    mode: 'text',
    args: [JSON.stringify(params)],
  };

  ps.PythonShell.run('models/gateway/analyticmodel.py', options, (err, results) => {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    // console.log('Model response: %j', results);
    updateModelRequestWithResponse(req, modelId, 'completed', results);
  });
}

/* Retrieve the list of known analytics model requests. */
router.get('/', (req, res) => {
  initUserSession(req);

  const allRequests = [];
  Object.keys(req.session.user.analytics).forEach((key) => {
    const item = Object.assign({}, req.session.user.analytics[key]);
    // interested in everything except the actual data
    item.data = undefined;
    allRequests.push(item);
  });

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(allRequests));
  return res.end();
});

/* Create a new analytic model request. */
router.post('/', (req, res) => {
  initUserSession(req);

  const modelRequest = {
    modelId: uuid(),
    status: 'new',
    request_date: new Date(),
    params: req.body.params,
  };

  req.session.user.analytics.push(modelRequest);

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(modelRequest));
  res.end();

  Promise.resolve()
    .then(() => invokeModelRequest(req, modelRequest.modelId, modelRequest.params));
});

/* Get an existing analytic model request. */
router.get('/:modelId', (req, res) => {
  initUserSession(req);

  const { modelId } = req.params;
  const modelRequest = getModelRequest(req, modelId);

  if (!modelRequest) {
    res.status(404);
    res.send('Unknown modelId');
    res.end();
    return;
  }

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(modelRequest));
  res.end();
});

/* Update an existing analytic model request. */
router.put('/:modelId', (req, res) => {
  initUserSession(req);

  const { params } = req.body;
  const { modelId } = req.params;
  let modelRequest = getModelRequest(req, modelId);
  if (!modelRequest) {
    res.status(404);
    res.send('Unknown modelId');
    res.end();
    return;
  }

  updateModelRequestWithNewRequest(req, modelId, 'new', params);

  modelRequest = getModelRequest(req, modelId);

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(modelRequest));
  res.end();

  Promise.resolve()
    .then(() => invokeModelRequest(req, modelId, params));
});

/* Persist an existing analytic model request against the current user.
 * Must have a current user context.
 */
router.post('/:modelId/persist', (req, res) => {
  // invoke picklet persist?
  res.send('Not implemented');
  res.end();
});

module.exports = router;
