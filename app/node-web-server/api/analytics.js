const DIR_ANALYTICS_FILES = "C:/workdir/analytics/";
let router = require('express').Router();
var fs = require('fs');
var ps = require('python-shell');

const bodyParser = require('body-parser');
router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json())

/* Retrieve the list of known analytics model responses. */
router.get('/', (req, res) => {
    res.writeHead(200, {'Content-Type': 'text/json'});
    fs.readdir(DIR_ANALYTICS_FILES, function(err, items) {
        if (err) throw err;
        let statResults = items.map( item => {
            if (item.endsWith(".json")) {
                var myfile = DIR_ANALYTICS_FILES + item;
                var stats = fs.statSync(myfile);
                var result = {};
                result.id = item.replace(".json", "");
                result.modified = stats["mtime"];
                result.size = stats["size"];
                return result;
            }
        });
        res.write(JSON.stringify(statResults));
        return res.end();
    });
});

router.post('/', (req, res) => {
    /*res.writeHead(200, {'Content-Type': 'text/json'});
    var uuid = require('uuid-random');
    var reqData = {};
    reqData.id = uuid();
    reqData.requestDate = new Date();
    var reqDataJson = JSON.stringify(reqData);
    fs.writeFile(DIR_ANALYTICS_FILES + reqData.id + ".json", reqDataJson, function(err) {
        if(err) {
            return console.log(err);
        }

        res.write(reqDataJson);
        res.end();
    });*/
    var options = {
        mode: 'text',
        args: [JSON.stringify(req.body.params)]
    };

    ps.PythonShell.run('../../models/gateway/analyticmodel.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('Model response: %j', results);
        res.write(JSON.stringify(results));
        res.end();
    }); 
});

module.exports = router;