import { Dispatch } from 'redux';
import { Article, IArticle } from '../../domain/articles';
import { ArticleService } from '../../domain/articles/article-service';
import { IPolaState } from '../types';
import * as actions from './articles-actions';

export const articlesDispatcher = {
  loadArticles: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    const articlesData = await ArticleService.getArticles();
    const articles = articlesData.results.map(data => new Article(data.title, data.text, data.date, data.photo));
    await dispatch(actions.LoadArticles(articles));
  },
};
