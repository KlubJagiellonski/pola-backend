import React from 'react';
import { Link } from 'gatsby';
import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import { IArticle } from '../domain/articles';
import { connect } from 'react-redux';
import ArticlesList from '../components/articles/ArticlesList';
import { IPolaState } from '../state/types';

interface NewsPage {
  articles?: IArticle[];
}

const NewsPage: React.FC<NewsPage> = ({ articles }) => (
  <PageLayout>
    <SEO title="Pola Web | Aktualności" />
    <ArticlesList articles={articles} width={600} />
    <Link to="/">Go back to the homepage</Link>
  </PageLayout>
);

export default connect((state: IPolaState) => ({
  articles: state.articles.data,
}))(NewsPage);
