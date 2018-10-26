/*
 * An API that facilitates uploading and downloading external data sources.
 */
const DIR_PROCESSED_FILES = './models/test/data_input_component_csv/';
const DIR_UPLOADED_FILES = './models/test/data_input_component_csv/';
const router = require('express').Router();
const formidable = require('formidable');
const fs = require('fs');
const XLSX = require('xlsx');

/* Logging method for this api. */
function log(requestType, msg) {
  console.log(`/api/source:${requestType}: ${msg}`);
}

/* Process an xslx at the given path. */
function processXslx(res, path) {
  const result = [];
  result.push({ msg: 'File upload accepted for processing.' });
  const workbook = XLSX.readFile(path);
  const sheetNameList = workbook.SheetNames;
  sheetNameList.forEach((sheetName) => {
    const worksheet = workbook.Sheets[sheetName];
    const csv = XLSX.utils.sheet_to_csv(worksheet);
    fs.writeFile(`${DIR_PROCESSED_FILES}${sheetName}.csv`, csv, (err) => {
      if (err) {
        log('POST', `Encountered error processing sheet ${sheetName}: ${err}`);
        result.push({ error_msg: `Encountered error processing sheet ${sheetName}: ${err}` });
      } else {
        log('POST', `Processed xslx sheet into saved csv: ${sheetName}`);
      }
    });
  });

  res.status(200).json(result);
  res.end();
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
      result.uri = `${req.originalUrl}/${result.name}`;
      return result;
    });
    res.write(JSON.stringify(statResults));
    return res.end();
  });
});

/* Retrieve a specific external data source file. */
router.get('/:filename', (req, res) => {
  const { filename } = req.params;
  const ext = filename.split('.').pop();

  // validations to make sure nothing naughty is attempted
  if(!filename || !filename.match(/^[\w\-. ]+$/g)) { // eslint-disable-line
    res.status(400).json({ error_msg: 'Unsupported filename' });
    res.end();
    return;
  }

  const filePath = DIR_PROCESSED_FILES + filename;
  try {
    const stat = fs.statSync(filePath);
    res.writeHead(200, {
      'Content-Type': `application/${ext}`,
      'Content-Disposition': `attachment;filename=${filename}`,
      'Content-Length': stat.size,
    });

    fs.createReadStream(filePath).pipe(res);
  } catch (err) {
    res.status(404).json({ error_msg: 'Unknown file' });
    res.end();
  }
});

/* Upload a new external data source XSLX, and process it. */
router.post('/', (req, res) => {
  const form = new formidable.IncomingForm();
  form.parse(req, (err, fields, files) => {
    if (err) {
      log('POST', `File upload error: ${err}`);
      res.status(200).json([{ error_msg: err }]);
      res.end();
      return;
    }

    const oldpath = files.filetoupload.path;
    const newpath = DIR_UPLOADED_FILES + files.filetoupload.name;
    // restrict supported file types
    if(!newpath || !newpath.match(/\.(xlsx)$/i)) { // eslint-disable-line
      res.status(200).json([{ error_msg: 'Unsupported file type - must be xslx' }]);
      res.end();
      return;
    }

    // move the upload to readable directory and process it
    fs.rename(oldpath, newpath, (err2) => {
      if (err2) {
        log('POST', `File processing error: ${err2}`);
        res.status(200).json({ error_msg: `File processing error: ${err2}` });
        res.end();
        return;
      }

      processXslx(res, newpath);
    });
  });
});

module.exports = router;
