import { Article } from '../../domain/articles';

export interface IArticlesTwoColumns {
  first: Article;
  second?: Article;
}

export function getArticlesTwoColumns(articles: Article[]) {
  const sortedArticles: IArticlesTwoColumns[] = [];
  let section: IArticlesTwoColumns[] = [];

  for (let i = 0; i < articles.length; i = i + 2) {
    if (articles[i + 1] !== undefined) {
      section.push({ first: articles[i], second: articles[i + 1] });
    } else {
      section.push({ first: articles[i] });
    }

    if (section.length === 3 || i + 2 >= articles.length) {
      sortedArticles.push(section.slice());
      section = [];
    }
  }

  return sortedArticles;
}

export function getVisibleArticles(actualArticleId: string, articles: Article[]) {
  let art = articles.slice();
  for (let i = 0; i < art.length; i++) {
    if (art[i].id === actualArticleId) {
      art.splice(i, 1);
    }
  }
  if (art.length > 3) {
    art = art.slice(0, 3);
  }

  return art;
}
