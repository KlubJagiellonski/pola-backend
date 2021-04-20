const apiPath = 'https://randomuser.me/api';

export interface IUser {
  gender: string;
  name: {
    title: string;
    first: string;
    last: string;
  };
  email: string;
  phone: string;
  nat: string;
}

interface IUsersResponse {
  results: IUser[];
  info: {
    seed: string;
    results: number;
    page: number;
    version: number;
  };
}

export interface ISearchParams {
  phrase: string;
}

export interface ISearchSuccess {
  results: string[];
}

export interface ISearchError {
  error: unknown;
}

export const SearchService = {
  getProducts: async (amount: number) => {
    const response = await fetch(`${apiPath}/?results=${amount}`);
    const productsJson: IUsersResponse = await response.json();
    return productsJson.results;
  },
};
