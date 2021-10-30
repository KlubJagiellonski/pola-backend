import { EAN, IProductData } from '../../domain/products';
import { SearchState, SearchStateName } from './search-reducer';

export namespace ProductSelectors {
  export const findProduct = (selectedCode: EAN, state: SearchState): IProductData | void => {
    let product: IProductData | undefined;
    if (state.stateName === SearchStateName.LOADED) {
      for (const page of state.resultPages) {
        const data = page.products.find((p) => p.code === selectedCode);
        if (data) {
          product = data;
          break;
        }
      }

      return product;
    }
  };
}
