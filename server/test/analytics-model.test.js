/*
 * A series of tests for the analytics model service.
 * Some of these requests require session context,
 * to mock an application user making consecutive requests.
 */
const analyticsModel = require('../service/analytics-model');

describe('Test the analytics model requests', () => {
  test('Check valid response model request', (done) => {
    analyticsModel.invokeModelRequest({ request_type: 'provider_profile', value: 'Psych' }, (err, responseJson) => {
      if (err) {
        console.log("damn, found error: " + err);
        console.log(JSON.stringify(responseJson));
        throw new Error(err);
      }
      expect(responseJson.response[0].header[0].provider_name).toBe('Psychiatrist');
      done();
    });
  });

  test('Check valid response model request for invalid arguments', (done) => {
    analyticsModel.invokeModelRequest({ myparam1: 'myvalue1' }, (err, responseJson) => {
      expect(responseJson.response[0].error_msg).toBe('ERROR: Could not parse argument: \'value\'');
      done();
    });
  });
});
