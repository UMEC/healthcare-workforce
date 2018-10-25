const request = require('supertest');
const app = require('../../server');

describe('Test the root path', () => {
  test('/api/source responds for GET method', (done) => {
    request(app).get('/api/source').then((response) => {
      expect(response.statusCode).toBe(200);
      done();
    });
  });
});

afterAll(() => { app.close(); });
