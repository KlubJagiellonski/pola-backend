import axios from 'axios';
import { IProductData, IProductMock } from '.';
import { ApiService } from '../../services/api-service';

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

const PRODUCT_SEARCH_API = 'https://fakestoreapi.com/products';

export class ProductService extends ApiService {
  public static getInstance(): ProductService {
    if (!ProductService.instance) {
      ProductService.instance = new ProductService();
    }
    return ProductService.instance;
  }
  private static instance: ProductService;

  private constructor() {
    super(PRODUCT_SEARCH_API);
  }

  private page: number = 0;

  public async searchProducts(phrase: string, token?: string): Promise<IProductSearchSuccess> {
    const amount = 5 + this.page;
    const response = await axios.get(`${this.apiUrl}?limit=${amount}`);
    const products: IProductMock[] = response.data;

    if (token) {
      this.page += 1;
    } else {
      this.page = 0;
    }

    return {
      nextPageToken: token || 'mock_token',
      totalItems: amount,
      products: products.map(mock => ({
        code: mock.id,
        name: mock.title,
        company: {
          name: mock.description,
        },
        brand: {
          name: mock.category,
        },
      })),
    };
  }
}
