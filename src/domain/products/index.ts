import { getNumber } from '../../utils/data/random-number';

export interface ICompany {
  name: string;
}

export interface IBrand {
  name: string;
}

export interface IProductData {
  code: string;
  name: string;
  company?: ICompany;
  brand?: IBrand;
}

export interface IProductEAN {
  id: string;
  title: string;
  description?: string;
  category?: string;
  image?: URL;
}

export interface IProductMock {
  id: string;
  title: string;
  description: string;
  category: string;
  image: URL;
}

export class Product implements IProductEAN {
  public id: string;
  public image: URL;

  constructor(public title: string, public description: string, public category: string, imageSrc: string) {
    this.id = `${getNumber()}-${getNumber()}-${getNumber()}-${getNumber()}`;
    this.image = new URL(imageSrc);
  }
}
