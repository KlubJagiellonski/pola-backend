import { Article } from '../../domain/articles';

export function getTagsList(articles: Article[]) {
  const cat: string[] = articles
    .map((el: Article) => {
      return el.tag;
    })
    .sort();
  const unique = new Set(cat);
  return Array.from(unique);
}
