import React from 'react';
import { Link } from 'gatsby';
import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { Article } from '../domain/articles';
import { connect, useDispatch } from 'react-redux';
import ArticlesList from '../components/articles/list/ArticlesList';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { PageType } from '../domain/website';

interface NewsPage {
  location?: Location;
  articles?: Article[];
}

const NewsPage: React.FC<NewsPage> = ({ location, articles }) => {
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.NEWS));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Aktualności" />
      <ArticlesList articles={articles} />
      <Link to="/">Go back to the homepage</Link>
    </PageLayout>
  );
};
export default connect((state: IPolaState) => ({
  articles: state.articles.data,
}))(NewsPage);
