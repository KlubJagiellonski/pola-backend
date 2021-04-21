export interface IProduct {
  id: string;
  title: string;
  description?: string;
  category?: string;
  image?: URL;
}

const getNumber = () => Math.floor(Math.random() * 1000);

export class Product implements IProduct {
  public id: string;
  public image: URL;

  constructor(public title: string, public description: string, public category: string, imageSrc: string) {
    this.id = `${getNumber()}-${getNumber()}-${getNumber()}-${getNumber()}`;
    this.image = new URL(imageSrc);
  }
}
