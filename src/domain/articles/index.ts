import { getGuid } from '../../utils/data/random-number';

export interface IArticle {
  id: string;
  title: string;
  content: string;
  date?: string;
  image?: string;
}

export class Article implements IArticle {
  public id: string;
  public image?: string;

  constructor(public title: string, public content: string, public date?: string, imageSrc?: string) {
    this.id = getGuid();
    this.image = imageSrc;
  }
}
