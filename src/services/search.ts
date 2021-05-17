import axios from 'axios';
import { ApiConnector } from './api-connector';

export interface ISearchParams {
  phrase: string;
}

export interface ISearchSuccess {
  results: IProductData[];
}

export interface ISearchError {
  error: unknown;
}

interface IProductData {
  id: number;
  title: string;
  description: string;
  category: string;
  image: string;
}

export class SearchService extends ApiConnector {
  public static getInstance(): SearchService {
    if (!SearchService.instance) {
      SearchService.instance = new SearchService();
    }
    return SearchService.instance;
  }
  private static instance: SearchService;

  private constructor() {
    super('https://fakestoreapi.com/products');
  }

  public async getProducts(amount: number): Promise<ISearchSuccess> {
    const response = await axios.get(`${this.apiUrl}?limit=${amount}`);
    return {
      results: response.data,
    };
  }
}
