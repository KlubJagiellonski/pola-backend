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

export const SearchService = {
  getProducts: async (amount: number) => {
    const response = await fetch(`${apiPath}/?results=${amount}`);
    const productsJson: IUsersResponse = await response.json();

    //   .then(response => response.json())
    //   .then((response: IUsersResponse) => {
    //     console.log('users', response.results.length);
    //     setUsers(response.results);
    //   });

    return productsJson.results;
  },
};
