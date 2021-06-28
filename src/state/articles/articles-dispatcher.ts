import { Dispatch } from 'redux';
import { Article } from '../../domain/articles';
import { IArticleEdge } from '../../domain/articles/article-service';
import { IPolaState } from '../types';
import * as actions from './articles-actions';

export const articlesDispatcher = {
  // loadArticles: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
  //   const articlesData = await ArticleService.getArticles();
  //   const articles = articlesData.results.map((data) => new Article(data.title, data.text, data.date, data.photo));
  //   await dispatch(actions.LoadArticles(articles));
  // },
  loadArticles: (edges: IArticleEdge[]) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    const articles = edges.reduce((articles: Article[], edge: IArticleEdge) => {
      const article = new Article(edge.node);
      return [...articles, article];
    }, []);
    //const articles = articlesData.map((node) => new Article(node));
    await dispatch(actions.LoadArticles(articles));
  },
};
