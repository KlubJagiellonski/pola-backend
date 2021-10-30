import axios, { AxiosResponse } from 'axios';
import { IProductData, ISearchSuccessResponse } from '.';
import { ApiAdapter } from '../../services/api-adapter';
import config from '../../app-config.json';
import { InvalidSearchResultError } from '../../services/api-errors';
import { ISearchResultPage } from '../../state/search/search-reducer';

export interface ISearchError {
  type: string;
  status: number;
  title: string;
  detail: string;
  instance?: string;
  errors?: string[];
}

const API_NAME = 'Search Product API';

export class ProductService extends ApiAdapter {
  public static getInstance(): ProductService {
    if (!ProductService.instance) {
      ProductService.instance = new ProductService();
    }
    return ProductService.instance;
  }
  private static instance: ProductService;

  private constructor() {
    super(API_NAME, config.searchEndpoint);
  }

  public async searchProducts(phrase: string, token?: string) {
    try {
      const searchQuery = this.buildSearchQuery(phrase, token);
      const response = await axios.get<ISearchSuccessResponse>(searchQuery);

      if (!response) {
        throw new Error('Response in empty');
      }
      if (response instanceof Error) {
        throw new Error('Got error response');
      }
      if (!this.isValidSearchResults(response)) {
        throw new InvalidSearchResultError();
      }

      return response.data;
    } catch (error: unknown) {
      const apiError = this.handleError(error);
      throw apiError;
    }
  }

  private buildSearchQuery(phrase: string, token?: string): string {
    let params = `query=${phrase}`;

    if (token) {
      params = params + `&pageToken=${token}`;
    }

    return `${this.apiUrl}?${params}`;
  }

  private isValidSearchResults(response: AxiosResponse): boolean {
    const responseBody = response.data;
    return responseBody?.totalItems !== undefined && !!responseBody?.products;
  }
}

/**
 * Reduces search result pages to one results collection
 * @param search API response data
 * @returns agreggated results collection
 */
export function reduceToFlatProductsList(pages: ISearchResultPage[]): IProductData[] {
  return pages.reduce((products: IProductData[], page: ISearchResultPage) => {
    return [...products, ...page.products];
  }, []);
}
