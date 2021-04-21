export interface IProduct {
  id: number;
  title: string;
  description?: string;
  category?: string;
  image?: URL;
}

export class Product implements IProduct {
  public id: number;
  public image: URL;

  constructor(public title: string, public description: string, public category: string, imageSrc: string) {
    this.id = Math.floor(Math.random() * 1000);
    this.image = new URL(imageSrc);
  }
}
