/*
 * An API that facilitates uploading and downloading external data sources.
 */
const router = require('express').Router();
const path = require('path');

/* Swagger specification index page. */
router.get('/', (req, res) => {
  res.sendFile(path.join(`${__dirname}/index.html`));
});

/* Administration page. */
router.get('/admin', (req, res) => {
  res.sendFile(path.join(`${__dirname}/admin.html`));
});

module.exports = router;
