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

  test('/api/source/:filename response for valid GET method', (done) => {
    server.get('/api/source').then((response) => {
      server.get(`/api/source/${response.body[0].name}`).then((getResponse) => {
        expect(getResponse.statusCode).toBe(200);
        done();
      });
    });
  });

  test('/api/source/:filename response for invalid GET method filename1', (done) => {
    server.get('/api/source/abcdefg').then((getResponse) => {
      expect(getResponse.statusCode).toBe(404);
      done();
    });
  });

  test('/api/source/:filename response for invalid GET method filename2', (done) => {
    server.get('/api/source/my%5Cfile.csv').then((getResponse) => {
      expect(getResponse.statusCode).toBe(400);
      done();
    });
  });

  test('/api/source/:filename response for invalid GET method filename3', (done) => {
    server.get('/api/source/my%2Ffile.csv').then((getResponse) => {
      expect(getResponse.statusCode).toBe(400);
      done();
    });
  });

  test('/api/source/:filename response for invalid GET method filename4', (done) => {
    server.get('/api/source/my$file.csv').then((getResponse) => {
      expect(getResponse.statusCode).toBe(400);
      done();
    });
  });

  test('/api/source response for valid POST method', (done) => {
    server.post('/api/source').attach('filetoupload', './models/data/Workforce Optimization Tool - Input Data.xlsx').then((response) => {
      expect(response.statusCode).toBe(200);
      expect(response.body).toHaveLength(1);
      expect(response.body[0].msg).toBe('File upload accepted for processing.');
      done();
    });
  }, 30000);

  test('/api/source response for invalid POST method', (done) => {
    server.post('/api/source').attach('filetoupload', './README.md').then((response) => {
      expect(response.statusCode).toBe(200);
      expect(response.body).toHaveLength(1);
      expect(response.body[0].error_msg).toBe('Unsupported file type - must be xslx');
      done();
    });
  });
});


beforeAll(() => {
  server = request(app);
});
