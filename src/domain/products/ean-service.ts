import axios from 'axios';
import { EAN, IProductEAN } from '.';
import { ApiAdapter } from '../../services/api-adapter';
import config from '../../app-config.json';
import { EmptyResponseDataError, FetchError } from '../../services/api-errors';

export interface IProductEANParams {
  code: EAN;
}

export interface IProductEANError {
  error: unknown;
}

const API_NAME = 'EAN Product API';

export class ProductEANService extends ApiAdapter {
  public static getInstance(): ProductEANService {
    if (!ProductEANService.instance) {
      ProductEANService.instance = new ProductEANService();
    }
    return ProductEANService.instance;
  }
  private static instance: ProductEANService;

  private constructor() {
    super(API_NAME, config.eanEndpoint);
  }

  private buildQuery(code: EAN): string {
    return `code=${code}&device_id="0"`;
  }

  public async getProduct(code: EAN): Promise<IProductEAN> {
    try {
      const query = this.buildQuery(code);
      const response = await await axios.get(`${this.apiUrl}?${query}`);
      const product: IProductEAN = response.data;

      if (!product) {
        throw new EmptyResponseDataError('EAN Product');
      }

      return product;
    } catch (e) {
      throw new FetchError(API_NAME, e);
    }
  }
}
