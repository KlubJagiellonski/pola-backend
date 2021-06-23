import React from 'react';
import { Link } from 'gatsby';
import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/SEO';
import { IArticle } from '../domain/articles';
import { connect, useDispatch } from 'react-redux';
import ArticlesList from '../components/articles/ArticlesList';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation } from '../state/app/app-actions';

interface NewsPage {
  location?: Location;
  articles?: IArticle[];
}

const NewsPage: React.FC<NewsPage> = ({ location, articles }) => {
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
    }
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web | Aktualności" />
      <ArticlesList articles={articles} width={600} />
      <Link to="/">Go back to the homepage</Link>
    </PageLayout>
  );
};
export default connect((state: IPolaState) => ({
  articles: state.articles.data,
}))(NewsPage);
