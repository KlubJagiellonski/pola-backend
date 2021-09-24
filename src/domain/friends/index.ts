import { IFriendNode } from './friend-service';

export class Friend {
  public id: string;
  public name: string;
  public image?: string;
  public description: string;
  public page: string;
  public slug?: string;

  constructor(data: IFriendNode) {
    this.id = data.id;
    this.name = data.name;
    this.image = data.image.base;
    this.description = data.description;
    this.page = data.page;
    this.slug = data.slug;
  }
}
