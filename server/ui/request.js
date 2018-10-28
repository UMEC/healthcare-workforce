/*
 * An API that facilitates uploading and downloading external data sources.
 */
const router = require('express').Router();
const path = require('path');

/* A page for testing file upload. */
router.get('/', (req, res) => {
  res.sendFile(path.join(`${__dirname}'/index.html`));
});

module.exports = router;
