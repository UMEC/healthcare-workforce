/*
 * An API that facilitates uploading and downloading external data sources.
 */
const router = require('express').Router();
const path = require("path");

/* Logging method for this api. */
function log(requestType, msg) {
  console.log(`/api/source:${requestType}: ${msg}`);
}

/* A page for testing file upload. */
router.get('/', (req, res) => {
  /*res.writeHead(200, { 'Content-Type': 'text/html' });
  res.write("<form action='../source/' method='post' enctype='multipart/form-data'>");
  res.write("<input type='file' name='filetoupload'><br>");
  res.write("<input type='submit'>");
  res.write('</form>');
  return res.end();*/
  res.sendFile(path.join(__dirname+'/index.html'));
});

module.exports = router;
