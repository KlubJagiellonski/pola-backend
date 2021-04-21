const apiPath = 'https://fakestoreapi.com/products';

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

export const SearchService = {
  getProducts: async (amount: number): Promise<ISearchSuccess> => {
    const response = await fetch(`${apiPath}?limit=${amount}`);
    const productsJson: IProductData[] = await response.json();
    return {
      results: productsJson,
    };
  },
};
