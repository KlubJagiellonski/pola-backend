import { useEffect } from 'react';
import { connect } from 'react-redux';
import { ArticleService, IArticleEdge } from '../domain/articles/article-service';
import { FriendsService, IFriendNode } from '../domain/friends/friend-service';
import { appDispatcher } from '../state/app/app-dispatcher';
import { articlesDispatcher } from '../state/articles/articles-dispatcher';
import { friendsDispatcher } from '../state/friends/friends-dispatcher';
import { IPolaState } from '../state/types';

interface IStateLoader {
  isArticlesLoaded?: boolean;
  isFriendsLoaded?: boolean;
  initApp?: () => void;
  loadArticles?: (edges: IArticleEdge[]) => void;
  loadFriends?: (node: IFriendNode[]) => void;
}

const Loader = (props: IStateLoader) => {
  const bootApplication = async () => {
    if (props.initApp) {
      await props.initApp();
    }
  };

  useEffect(() => {
    bootApplication();
  }, []);

  const queryResultFriend = FriendsService.getAll();
  if (!props.isFriendsLoaded && queryResultFriend?.allLogosFriendsYaml?.nodes && props.loadFriends) {
    const data = queryResultFriend.allLogosFriendsYaml.nodes;
    props.loadFriends(data);
  }

  const queryResult = ArticleService.getAll();
  if (!props.isArticlesLoaded && queryResult?.allMarkdownRemark?.edges && props.loadArticles) {
    const data = queryResult.allMarkdownRemark.edges;
    data.sort((a: IArticleEdge, b: IArticleEdge) => {
      return Date.parse(b.node.fields.prefix) - Date.parse(a.node.fields.prefix);
    });
    props.loadArticles(data);
  }

  return null;
};

export const StateLoader = connect(
  (state: IPolaState) => ({
    isArticlesLoaded: state.articles.initialized,
    isFriendsLoaded: state.friends.initialized,
  }),
  {
    initApp: appDispatcher.initialize,
    loadArticles: articlesDispatcher.loadArticles,
    loadFriends: friendsDispatcher.loadFriends,
  }
)(Loader);
