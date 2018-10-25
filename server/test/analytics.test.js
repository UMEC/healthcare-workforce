/*
 * A series of tests for the analytics model service.
 * Some of these requests require session context,
 * to mock an application user making consecutive requests.
 */
const request = require('supertest');
const session = require('supertest-session');
const app = require('../../server');

let server;
let testSession;

describe('Test the analytics API', () => {
  test('/api/analytics valid response for GET method', (done) => {
    server.get('/api/analytics').then((response) => {
      expect(response.statusCode).toBe(200);
      done();
    });
  });

  test('/api/analytics valid response for POST method', (done) => {
    server.post('/api/analytics').send({ params: { type: 'cost_quality_adjustment', value: 0.5 } }).then((response) => {
      expect(response.statusCode).toBe(200);
      expect(response.body.params.type).toBe('cost_quality_adjustment');
      done();
    });
  });

  test('/api/analytics/{modelId} valid response for GET method', (done) => {
    testSession.post('/api/analytics').send({ params: { type: 'some_random_input_type', value: 0.5 } }).then((response) => {
      testSession.get(`/api/analytics/${response.body.modelId}`).then((getResponse) => {
        expect(getResponse.statusCode).toBe(200);
        expect(getResponse.body.params.type).toBe('some_random_input_type');
        done();
      });
    });
  });

  test('/api/analytics/{modelId} 404 response for GET method', (done) => {
    testSession.get('/api/analytics/abcdefgh').then((getResponse) => {
      expect(getResponse.statusCode).toBe(404);
      done();
    });
  });

  test('/api/analytics/{modelId} valid response for PUT method', (done) => {
    testSession.post('/api/analytics').send({ params: { type: 'some_random_input_type', value: 0.5 } }).then((response) => {
      testSession.put(`/api/analytics/${response.body.modelId}`)
        .send({ params: { type: 'the_second_input_type', value: 0.5 } }).then((putResponse) => {
          expect(putResponse.statusCode).toBe(200);
          expect(putResponse.body.params.type).toBe('the_second_input_type');
          done();
        });
    });
  });

  test('/api/analytics/{modelId} 404 response for PUT method', (done) => {
    testSession.put('/api/analytics/abcdefgh').then((getResponse) => {
      expect(getResponse.statusCode).toBe(404);
      done();
    });
  });
});

beforeAll(() => {
  server = request(app);
  testSession = session(app);
});
