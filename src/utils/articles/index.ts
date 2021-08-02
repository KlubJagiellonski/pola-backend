import { Article } from '../../domain/articles';

export interface IArticlesTwoColumns {
  first: Article[];
  second: Article[];
}

export function getArticlesTwoColumns(articles: Article[]) {
  const sortedArticles: IArticlesTwoColumns[] = [];
  let firstColumn: Article[] = [];
  let secondColumn: Article[] = [];
  let currentColumn: number = 1;

  for (let i = 0; i < articles.length; i++) {
    if (i % 6 === 0) {
      currentColumn = 1;
    } else if (i % 3 === 0) {
      currentColumn = 2;
    }

    if (currentColumn === 1) {
      firstColumn.push(articles[i]);
      currentColumn = 2;
    } else {
      secondColumn.push(articles[i]);
      currentColumn = 1;
    }

    if (firstColumn.length + secondColumn.length === 6) {
      sortedArticles.push({ first: firstColumn.slice(), second: secondColumn.slice() });
      firstColumn = [];
      secondColumn = [];
    }
  }
  if (firstColumn.length + secondColumn.length !== 6) {
    sortedArticles.push({ first: firstColumn.slice(), second: secondColumn.slice() });
  }

  return sortedArticles;
}
