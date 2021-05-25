import { getGuid } from '../../utils/data/random-number';

export interface IFriend {
  id: string;
  description: string;
  image?: string;
}

export class Friend implements IFriend {
  public id: string;
  public image?: string;

  constructor(public description: string, imageSrc?: string) {
    this.image = imageSrc;
    this.id = getGuid();
  }
}
