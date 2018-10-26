const request = require('supertest');
const app = require('../../server');

let server;

describe('Test the source API', () => {
  test('/api/source response for valid GET method', (done) => {
    server.get('/api/source').then((response) => {
      expect(response.statusCode).toBe(200);
      expect(response.body.length).not.toBe(0);
      expect(response.body[0].name).toBeDefined();
      done();
    });
  });

  test('/api/source response for valid POST method', (done) => {
    server.post('/api/source').attach('filetoupload', './models/test/Workforce Optimization Tool - Input Data.xlsx').then((response) => {
      expect(response.statusCode).toBe(200);
      expect(response.body.length).toBe(1);
      expect(response.body[0].msg).toBe('File upload accepted for processing.');
      done();
    });
  }, 30000);

  test('/api/source response for invalid POST method', (done) => {
    server.post('/api/source').attach('filetoupload', './README.md').then((response) => {
      expect(response.statusCode).toBe(200);
      expect(response.body.length).toBe(1);
      expect(response.body[0].error_msg).toBe('Unsupported file type - must be xslx');
      done();
    });
  });
});


beforeAll(() => {
  server = request(app);
});
