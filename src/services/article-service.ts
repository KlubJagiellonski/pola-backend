export interface IArticlesSuccess {
  results: IArticleData[];
}

export interface IArticlesError {
  error: unknown;
}

interface IArticleData {
  id: number;
  title: string;
  text: string;
  date: string;
  photo: string;
}

const articles: IArticleData[] = [
  {
    id: 1,
    title: 'ŚWIĄTECZNE ZAKUPY Z POLA APP DO 15% TANIEJ',
    text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
    date: '2020-12-12',
    photo: 'xmas.png',
  },
  {
    id: 2,
    title: 'WIELKANOCNE ZAKUPY Z POLA APP DO 60% TANIEJ',
    text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
    date: '2021-03-17',
    photo: 'xmas.png',
  },
  {
    id: 3,
    title: 'MAJÓWKA Z POLA APP DO 45% TANIEJ',
    text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
    date: '2021-04-21',
    photo: 'xmas.png',
  },
];

export const ArticleService = {
  getArticles: async (): Promise<IArticlesSuccess> => {
    return {
      results: articles,
    };
  },
};
