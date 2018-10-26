/* Directories for file uploading and processing */
const DIR_PROCESSED_FILES = './models/test/data_input_component_csv/';
const DIR_UPLOADED_FILES = './';
const router = require('express').Router();
const formidable = require('formidable');
const fs = require('fs');
const XLSX = require('xlsx');

/* Logging method for this api. */
function log(requestType, msg) {
  console.log(`/api/source:${requestType}: ${msg}`);
}

/* A temporary helper service for testing file upload. */
router.get('/upload', (req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.write("<form action='./' method='post' enctype='multipart/form-data'>");
  res.write("<input type='file' name='filetoupload'><br>");
  res.write("<input type='submit'>");
  res.write('</form>');
  return res.end();
});

/* Retrieve the list of known external data source files. */
router.get('/', (req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  fs.readdir(DIR_PROCESSED_FILES, (err, items) => {
    if (err) throw err;
    const statResults = items.map((item) => {
      const myfile = DIR_PROCESSED_FILES + item;
      const stats = fs.statSync(myfile);
      const result = {};
      result.name = item;
      result.modified = stats.mtime;
      result.size = stats.size;
      return result;
    });
    res.write(JSON.stringify(statResults));
    return res.end();
  });
});

/* Upload a new external data source XSLX, and process it. */
router.post('/', (req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  const form = new formidable.IncomingForm();
  form.parse(req, (err, fields, files) => {
    if (err) {
      log('POST', `File upload error: ${err}`);
      res.write(JSON.stringify([{ error_msg: err }]));
      res.end();
      return;
    }

    const oldpath = files.filetoupload.path;
    const newpath = DIR_UPLOADED_FILES + files.filetoupload.name;
    // restrict supported file types
    if(!newpath || !newpath.match(/\.(xlsx)$/i)) { // eslint-disable-line
      res.write(JSON.stringify([{ error_msg: 'Unsupported file type - must be xslx' }]));
      res.end();
      return;
    }

    // move the upload to readable directory and process it
    fs.rename(oldpath, newpath, (err2) => {
      const result = [];
      result.push({ msg: 'File upload accepted for processing.' });
      if (!err2) {
        const workbook = XLSX.readFile(newpath);
        const sheetNameList = workbook.SheetNames;
        sheetNameList.forEach((sheetName) => {
          const worksheet = workbook.Sheets[sheetName];
          const csv = XLSX.utils.sheet_to_csv(worksheet);
          fs.writeFile(`${DIR_PROCESSED_FILES}${sheetName}.csv`, csv, (err3) => {
            if (err3) {
              log('POST', `Encountered error processing sheet ${sheetName}: ${err3}`);
              result.push({ error_msg: `Encountered error processing sheet ${sheetName}: ${err3}` });
            } else {
              // success case, the file was saved
              log('POST', `Processed xslx sheet into saved csv: ${sheetName}`);
            }
          });
        });
      } else {
        log('POST', `File processing error: ${err2}`);
        result.push({ error_msg: `File processing error: ${err2}` });
      }
      res.write(JSON.stringify(result));
      res.end();
    });
  });
});

module.exports = router;
