/*
 * A series of tests for requests to the underlying analytics model engine.
 */
const analyticsModel = require('../service/analytics-model');

describe('Test analytics model requests', () => {
  test('Check valid response model request', (done) => {
    analyticsModel.invokeModelRequest({ request_type: 'provider_profile', value: 'Psych' }, (err, responseJson) => {
      if (err) throw new Error(err);
      if (responseJson.response.error_msg) throw new Error(responseJson.response.error_msg);

      expect(responseJson.response.provider.provider_name).toBe('Psychiatrist');
      done();
    });
  });

  test('Check valid response model request for invalid arguments', (done) => {
    analyticsModel.invokeModelRequest({ myparam1: 'myvalue1' }, (err, responseJson) => {
      expect(responseJson.response.error_msg).toBe('ERROR: Could not parse argument: \'value\'');
      done();
    });
  });
});
