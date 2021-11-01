import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { margin, Device } from '../styles/theme';
import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { Article } from '../domain/articles';
import { connect, useDispatch } from 'react-redux';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { PageType } from '../domain/website';
import { PageSection } from '../layout/PageSection';
import './../components/Pagination.css';
import SocialMedia from '../components/social-media/SocialMedia';
import TagsList from '../components/tags/TagsList';
import { ArrayParam, withDefault, useQueryParams, NumberParam } from 'use-query-params';
import { getTagsList } from './../utils/tags';
import NewsPageArticles from '../components/articles/list/NewsPagesArticles';
import Placeholder from '../components/Placeholder';

const Title = styled.p`
  margin-top: ${margin.veryBig};
  font-weight: bold;

  @media ${Device.mobile} {
    display: none;
  }
`;

const InfoSection = styled.div`
  display: flex;
  margin: ${margin.normal} 0;

  div {
    flex: 1;
  }

  @media ${Device.mobile} {
    flex-direction: column;
  }
`;

interface NewsPage {
  location?: Location;
  articles?: Article[];
}

interface IQuery {
  tags: string[];
  id: number;
}

const NewsPage: React.FC<NewsPage> = ({ location, articles }) => {
  const [tag, setTag] = useState<string[]>([]);
  const dispatch = useDispatch();
  const [query, setQuery] = useQueryParams<IQuery>({
    tags: withDefault(ArrayParam, []),
    id: NumberParam,
  });

  useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.NEWS));
    }
  }, []);

  useEffect(() => {
    if (articles) {
      setTag(getTagsList(articles));
    }
    document.querySelector('body').scrollTo(0, 0);
  }, [articles, query]);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Aktualności" />
      <Placeholder text="Aktualności" />
      <PageSection>
        <NewsPageArticles articles={articles} query={query} setQuery={setQuery} />
        <InfoSection>
          <TagsList tag={tag} activeTags={query.tags} />
          <SocialMedia />
        </InfoSection>
      </PageSection>
    </PageLayout>
  );
};
export default connect((state: IPolaState) => ({
  articles: state.articles.data,
}))(NewsPage);
