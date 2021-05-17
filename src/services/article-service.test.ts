const mockFailureResponse = 'Something bad happened!';

/*
 * Example of mocking a function that was imported into the system under test.
 * The mock must be declared before importing the SUT file, hence the two test fies.
 */
jest.mock('./article-service', () => ({
  getArticles: () => {
    return Promise.reject(mockFailureResponse);
  },
}));

import { ArticleService } from './article-service';

describe('Article Service', () => {
  it('should return a promise containing a data', async () => {
    const result = await ArticleService.getArticles();
    expect(result).toEqual(mockFailureResponse);
  });
});
