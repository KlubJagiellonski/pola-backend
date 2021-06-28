import { IArticleNode } from './article-service';

export class Article {
  public id: string;
  public title: string;
  public subTitle: string;
  public slug: string;
  public date?: string;
  public imagePath?: string;

  constructor(data: IArticleNode) {
    this.id = data.id;
    this.title = data.frontmatter.title;
    this.subTitle = data.frontmatter.subTitle;
    this.slug = data.fields.slug;
    this.date = data.fields.prefix;
    this.imagePath = data.frontmatter.cover.relativePath;
  }
}
