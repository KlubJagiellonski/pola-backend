import { useEffect } from 'react';
import { connect } from 'react-redux';
import { ArticleService, IArticleEdge } from '../domain/articles/article-service';
import { appDispatcher } from '../state/app/app-dispatcher';
import { articlesDispatcher } from '../state/articles/articles-dispatcher';
import { friendsDispatcher } from '../state/friends/friends-dispatcher';
import { IPolaState } from '../state/types';

interface IStateLoader {
  isArticlesLoaded?: boolean;
  initApp?: () => void;
  loadArticles?: (edges: IArticleEdge[]) => void;
  loadFriends?: () => void;
}

export const StateLoader = (props: IStateLoader) => {
  const bootApplication = async () => {
    if (props.initApp) {
      await props.initApp();
    }
    if (props.loadFriends) {
      await props.loadFriends();
    }
  };

  useEffect(() => {
    bootApplication();
  }, []);

  const queryResult = ArticleService.getAll();
  if (!props.isArticlesLoaded && queryResult?.allMarkdownRemark?.edges && props.loadArticles) {
    const data = queryResult.allMarkdownRemark.edges;
    data.sort((a : IArticleEdge, b : IArticleEdge)=>{
        return Date.parse(b.node.fields.prefix) - Date.parse(a.node.fields.prefix);
    })
    props.loadArticles(data);
  }

  return null;
};

export const StateLoader2 = connect(
  (state: IPolaState) => ({
    isArticlesLoaded: state.articles.initialized,
  }),
  {
    initApp: appDispatcher.initialize,
    loadArticles: articlesDispatcher.loadArticles,
    loadFriends: friendsDispatcher.loadFriends,
  }
)(StateLoader);
