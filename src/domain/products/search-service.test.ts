import Sinon from 'sinon';
import { expect } from 'chai';
import { ProductService } from './search-service';
import axios, { AxiosError, AxiosResponse } from 'axios';
import { ISearchSuccessResponse } from '.';
import { mockGETRequest, mockAxiosErrorResponse, mockProduct } from '../../utils/tests/mocks';
import { NetworkError } from '../../services/api-errors';

const mockSearchResult = (): ISearchSuccessResponse => ({
  nextPageToken: 'bcvsag456345345',
  totalItems: 13,
  products: [mockProduct(), mockProduct(), mockProduct(), mockProduct()],
});

const mockSearchResponse = (headers?: any): AxiosResponse => ({
  data: mockSearchResult(),
  status: 200,
  statusText: 'OK',
  headers,
  config: mockGETRequest(),
  request: {},
});

const mockEmptyQueryErrorResponse = (): AxiosError =>
  mockAxiosErrorResponse(400, 'Bad request', {
    type: 'about:blank',
    title: 'Request validation failed',
    detail: '1 errors encountered',
    status: 400,
    errors: ['Value of parameter cannot be empty: query'],
  });

const mockNetworkErrorResponse = (): AxiosError => {
  const error = mockAxiosErrorResponse(503, 'Service unavailable', {
    type: 'connection:failed',
    title: 'Service connecition failed',
    detail: '1 errors encountered',
    status: 503,
  });

  delete error.request;
  delete error.response;

  return error;
};

const mockServiceErrorResponse = (): AxiosError => {
  const error = mockAxiosErrorResponse(500, 'Internal service error', {
    type: 'service:fail',
    title: 'Service internal failure',
    detail: '1 errors encountered',
    status: 500,
  });

  return error;
};

describe('Product search service', () => {
  let getProducts: Sinon.SinonStub;

  beforeEach(() => {
    getProducts = Sinon.stub(axios, 'get');
  });

  afterEach(() => {
    getProducts.restore();
  });

  describe('for correct query', () => {
    it('should response valid search results object', async () => {
      getProducts.resolves(mockSearchResponse());

      const responseData = await ProductService.getInstance().searchProducts('some query');

      expect(responseData, 'response data should be an object').not.undefined;
      expect(responseData?.totalItems).equals(13, 'icorrect total number of items');
      expect(responseData?.products.length).equals(4, `incorrect number of page's items`);
      expect(responseData?.nextPageToken, 'next page token should be defined').not.undefined;
    });
  });

  describe('for empty query', () => {
    it('should return a valid empty collection', async () => {
      getProducts.throws(mockEmptyQueryErrorResponse());

      const responseData = await ProductService.getInstance().searchProducts('');

      expect(responseData, 'response data should be an object').not.undefined;
      expect(responseData?.totalItems).equals(0, 'should not be items for empty query');
      expect(responseData?.products.length).equals(0, 'should not be products for empty query');
      expect(responseData?.nextPageToken, 'should not be next page token for empty query').null;
    });
  });

  describe('for invalid search result', () => {
    it('should throw an invalid data error', async () => {
      getProducts.resolves({ invalidProperty: 1 });

      try {
        await ProductService.getInstance().searchProducts('some valid query');
      } catch (e: any) {
        expect(e instanceof Error).is.true;
        expect(e.name).equals('Invalid search result');
      }
    });
  });

  describe('for network error', () => {
    it('should throw a network error when search service in unreachable', async () => {
      getProducts.resolves(mockNetworkErrorResponse());

      try {
        await ProductService.getInstance().searchProducts('some valid query');
      } catch (e: any) {
        expect(e instanceof Error).is.true;
        expect(e.name).equals('Network error');
      }
    });
  });

  describe('for error response', () => {
    it('should throw an internal service error', async () => {
      getProducts.resolves(mockServiceErrorResponse());

      try {
        await ProductService.getInstance().searchProducts('some valid query');
      } catch (e: any) {
        expect(e instanceof Error).is.true;
        expect(e.name).equals('Internal service error');
      }
    });
  });
});
