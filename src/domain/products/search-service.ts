import axios from 'axios';
import { IProductData, IProductMock } from '.';
import { ApiService } from '../../services/api-service';
import { getEAN, getNumber } from '../../utils/data/random-number';
import config from '../../app-config.json';
import { EmptyResponseDataError, FetchError } from '../../services/api-errors';

export interface ISearchParams {
  phrase: string;
}

export interface IProductSearchSuccess {
  nextPageToken: string;
  totalItems: number;
  products: IProductData[];
}

export interface ISearchError {
  error: unknown;
}

export class ProductService extends ApiService {
  public static getInstance(): ProductService {
    if (!ProductService.instance) {
      ProductService.instance = new ProductService();
    }
    return ProductService.instance;
  }
  private static instance: ProductService;

  private constructor() {
    super(config.searchApiURL);
  }

  private page: number = 0;

  public async searchProducts(phrase: string, token?: string): Promise<IProductSearchSuccess> {
    try {
      const amount = 5 + this.page;
      const response = await axios.get(`${this.apiUrl}?limit=${amount}`);
      const products: IProductMock[] = response.data;

      if (!products) {
        throw new EmptyResponseDataError('products');
      }

      if (token) {
        this.page += 1;
      } else {
        this.page = 0;
      }

      return {
        nextPageToken: token || 'mock_token',
        totalItems: amount,
        products: products.map(
          mock =>
            ({
              id: mock.id.toString(),
              code: getEAN(),
              name: mock.title,
              company: {
                name: mock.description,
              },
              brand: {
                name: mock.category,
              },
              score: getNumber(0, 100),
            } as IProductData)
        ),
      };
    } catch (e) {
      throw new FetchError('Search API', e);
    }
  }
}
