import { getNumber } from '../../utils/data/random-number';

export interface IProduct {
  id: string;
  title: string;
  description?: string;
  category?: string;
  image?: URL;
}

export class Product implements IProduct {
  public id: string;
  public image: URL;

  constructor(public title: string, public description: string, public category: string, imageSrc: string) {
    this.id = `${getNumber()}-${getNumber()}-${getNumber()}-${getNumber()}`;
    this.image = new URL(imageSrc);
  }
}
