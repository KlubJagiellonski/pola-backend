import { ProductEANService } from './ean-service';

const mockFailureResponse = 'Something bad happened!';

/*
 * Example of mocking a function that was imported into the system under test.
 * The mock must be declared before importing the SUT file, hence the two test fies.
 */
// jest.mock('./ean-service', () => ({
//   getProduct: (code: EAN) => {
//     return Promise.reject(mockFailureResponse);
//   },
// }));

// describe('Product EAN service', () => {
//   it('should return a promise containing a data', async () => {
//     const result = await ProductEANService.getInstance().getProduct('4006985902304', 2);
//     expect(result).toEqual(mockFailureResponse);
//   });
// });
