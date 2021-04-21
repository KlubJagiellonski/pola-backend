import { IArticle } from '../../domain/articles';
import { IAction } from '../types';

export const actionTypes = {
  LOAD_ARTICLES: 'ARTICLES:LOAD',
};

export const LoadArticles = (articles: IArticle[]): IAction => ({
  type: actionTypes.LOAD_ARTICLES,
  payload: {
    articles,
  },
});
