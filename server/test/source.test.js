const request = require('supertest');
const app = require('../../server');

let server;

describe('Test the root path', () => {
  test('/api/source responds for GET method', (done) => {
    server.get('/api/source').then((response) => {
      expect(response.statusCode).toBe(200);
      done();
    });
  });
});

beforeAll(() => {
  server = request(app);
});
