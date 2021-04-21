const mockFailureResponse = 'Something bad happened!';

/*
 * Example of mocking a function that was imported into the system under test.
 * The mock must be declared before importing the SUT file, hence the two test fies.
 */
jest.mock('./search-service', () => ({
  getProducts: (amount: string) => {
    return Promise.reject(mockFailureResponse);
  },
}));

import { SearchService } from './search-service';

describe('Search Service', () => {
  it('should return a promise containing a data', async () => {
    const result = await SearchService.getProducts(10);
    expect(result).toEqual(mockFailureResponse);
  });
});
