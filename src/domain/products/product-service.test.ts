import { ProductService } from './product-service';

const mockFailureResponse = 'Something bad happened!';

/*
 * Example of mocking a function that was imported into the system under test.
 * The mock must be declared before importing the SUT file, hence the two test fies.
 */
jest.mock('./product-service', () => ({
  searchProducts: (phrase: string, token?: string) => {
    return Promise.reject(mockFailureResponse);
  },
}));

describe('Search Service', () => {
  it('should return a promise containing a data', async () => {
    const result = await ProductService.getInstance().searchProducts('some query', 'token');
    expect(result).toEqual(mockFailureResponse);
  });
});
