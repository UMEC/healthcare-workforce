const router = require('express').Router();
const bodyParser = require('body-parser');

router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());

function initUserSession(req) {
  if (!req.session.user) {
    req.session.user = {};
  }
}

function getUserSession(req) {
  initUserSession(req);
  return {
    authenticated_user: req.session.user.user_email,
    state: req.session.user.state,
  };
}

function validatePost(req, res) {
  if (!req.body) {
    res.status(400);
    res.send('Missing payload');
    return false;
  }

  return true;
}

router.get('/session', (req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(getUserSession(req)));
  res.end();
});


router.post('/session', (req, res) => {
  if (!validatePost(req, res)) {
    return;
  }

  initUserSession(req);
  req.session.user.state = req.body.state;

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(getUserSession(req)));
  res.end();
});


router.post('/auth', (req, res) => {
  if (!validatePost(req, res)) {
    return;
  }

  initUserSession(req);
  req.session.user.user_email = req.body.user_email;

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.write(JSON.stringify(getUserSession(req)));
  res.end();
});

/* Logout - clear the user's session. */
router.get('/logout', (req, res) => {
  req.session.user = {};
  res.end();
});

module.exports = router;
