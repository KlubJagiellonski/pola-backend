import { AxiosError, AxiosRequestConfig } from 'axios';
import { IProductData } from '../../domain/products';

export const mockAxiosErrorResponse = (status: number, statusText: string, data?: any, request?: any): AxiosError => ({
  config: mockGETRequest(),
  code: status.toString(),
  request,
  response: {
    status,
    statusText,
    headers: {
      xFrameOptions: 'DENY',
      contentLength: 167,
      contentLanguage: 'pl',
      vary: 'Accept-Language',
      referrerPolicy: 'same-origin',
      via: '1.1 vegur',
    },
    config: mockGETRequest(),
    data,
  },
  isAxiosError: true,
  name: 'test name',
  message: statusText,
  toJSON: () => ({}),
});

export const mockGETRequest = (headers?: any, params?: any): AxiosRequestConfig => ({
  url: 'mock.server.com',
  method: 'GET',
  headers,
  params,
});

export const mockProduct = (): IProductData => ({
  code: 'EAN4534',
  name: 'test product',
  score: 55,
  polishCapital: 55,
  company: {
    name: 'test company',
  },
  brand: {
    name: 'test brand',
  },
});
