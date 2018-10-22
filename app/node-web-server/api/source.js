/* Directories for file uploading and processing */
const DIR_PROCESSED_FILES = "C:/workdir/processed/";
const DIR_UPLOADED_FILES = "C:/workdir/upload/";

let router = require('express').Router();
var formidable = require('formidable');
var fs = require('fs');
if(typeof require !== 'undefined') XLSX = require('xlsx');
 
/* A temporary helper service for testing file upload. */
router.get('/upload', (req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('<form action="./" method="post" enctype="multipart/form-data">');
    res.write('<input type="file" name="filetoupload"><br>');
    res.write('<input type="submit">');
    res.write('</form>');
    return res.end();
});

/* Retrieve the list of known external data source files. */
router.get('/', (req, res) => {
    res.writeHead(200, {'Content-Type': 'text/json'});
    fs.readdir(DIR_PROCESSED_FILES, function(err, items) {
        if (err) throw err;
        let statResults = items.map( item => {
            var myfile = DIR_PROCESSED_FILES + item;
            var stats = fs.statSync(myfile);
            var result = {};
            result.name = item;
            result.modified = stats["mtime"];
            result.size = stats["size"];
            return result;
        });
        res.write(JSON.stringify(statResults));
        return res.end();
    });
});

/* Upload a new external data source XSLX, and process it. */
router.post('/', (req, res) => {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
      var oldpath = files.filetoupload.path;
      var newpath = DIR_UPLOADED_FILES + files.filetoupload.name;
      // restrict supported file types
      if(!newpath || !newpath.match(/\.(xlsx)$/i)) {
        res.write('Unsupported file type - must be xslx');
        res.end();
        return;
      }
          
      // move the upload to readable directory and process it
      fs.rename(oldpath, newpath, function (err) {
        res.write('File upload accepted for processing.');
        if (!err) {
            var workbook = XLSX.readFile(newpath);
            var sheet_name_list = workbook.SheetNames;
            sheet_name_list.forEach(function(sheetName) {
                var worksheet = workbook.Sheets[sheetName];
                var csv = XLSX.utils.sheet_to_csv(worksheet)
                fs.writeFile(DIR_PROCESSED_FILES + sheetName + ".csv", csv, (err) => {  
                    if (err) throw err;
                
                    // success case, the file was saved
                    console.log('Processed sheet into saved csv: ' + sheetName);
                });
            });
        } else {
            console.log(err);
            res.write(err);
        }
        res.end();
      });
    });
});

module.exports = router;