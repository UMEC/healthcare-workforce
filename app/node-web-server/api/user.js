let router = require('express').Router();
var session = require('express-session')
var uuid = require('uuid-random');
const bodyParser = require('body-parser');
router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json())

var sess = {
    genid: function(req) {
        return uuid() // use UUIDs for session IDs
    },
    secret: 'mousemonkey',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}
if (router.get('env') === 'production') {
    router.set('trust proxy', 1) // trust first proxy 
    sess.cookie.secure = true // serve secure cookies
}  
router.use(session(sess));
 
// Access the session as req.session
router.get('/session', function(req, res, next) {
    res.write(JSON.stringify(getUserSession(req)));
    res.end();
})


router.post('/session', (req, res) => {
    if (!validatePost(req, res)) {
        return;
    }
    
    req.session.state = req.body.state;
    
    res.write(JSON.stringify(getUserSession(req)));
    res.end();
});

router.post('/auth', (req, res) => {
    if (!validatePost(req, res)) {
        return;
    }
    
    req.session.user_email = req.body.user_email;
    
    res.write(JSON.stringify(getUserSession(req)));
    res.end();
});

function getUserSession(req) {
    return {
        "authenticated_user" : req.session.user_email,
        "state" : req.session.state
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

module.exports = router; 