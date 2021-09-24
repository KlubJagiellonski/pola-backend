import React, { useEffect } from 'react';
import styled from 'styled-components';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../../layout/PageLayout';
import SEOMetadata from '../../utils/browser/SEOMetadata';
import { IPolaState } from '../../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../../state/app/app-actions';
import { PageType } from '../../domain/website';
import { PageSection } from '../../layout/PageSection';
import { ArticleHeader } from './ArticleHeader';
import { Device, margin } from '../../styles/theme';
import { Article } from '../../domain/articles';
import SideInformations from '../SideInformations';
import { Friend } from '../../domain/friends';

const Content = (props: any) => {
  const { html, children } = props;

  if (html) {
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
  } else {
    return <div>{children}</div>;
  }
};

interface IArticlePage {
  location?: Location;
  article: any;
  articles: Article[];
  friends: Friend[];
  author?: any;
  slug?: string;
  facebook?: any;
  cover?: any;
}

const Wrapper = styled.div`
  display: flex;
  gap: ${margin.veryBig};
  margin-top: ${margin.veryBig};

  @media ${Device.mobile} {
    display: inline;
    gap: 0;
  }
`

const FirstColumn = styled.div`
  flex: 3;
  flex-basis: 0;

  @media ${Device.mobile} {
    margin-top: ${margin.veryBig};

  }
`

const SecondColumn = styled.div`
  flex: 1;
  flex-basis: 0;
`

const ArticlePage = (props: IArticlePage) => {
  const { location, article, author, slug, facebook, articles, friends } = props;
  const title = ((article || {}).frontmatter || {}).title;
  const subTitle = ((article || {}).frontmatter || {}).subTitle;
  const category = ((article || {}).frontmatter || {}).category;
  const date = ((article || {}).fields || {}).prefix;
  const html = (article || {}).html;
  const fluid = ((article || {}).frontmatter || {}).cover.childImageSharp.fluid;

  const dispatch = useDispatch();

  useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.ARTICLE));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle={`Pola Web | ${title}`} />
      <PageSection>
        <Wrapper>
          <FirstColumn>
            <PageSection>
              <ArticleHeader
                title={title}
                subTitle={subTitle}
                date={date}
                fluid={fluid}
                category={category}
              />
            </PageSection>
            <PageSection>
              <Content html={html} />
            </PageSection>
          </FirstColumn>
          <SecondColumn>
            <SideInformations actualArticleId={article.id} articles={articles} friends={friends} />
          </SecondColumn>
        </Wrapper>
      </PageSection>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({
  location: state.app.location,
  articles: state.articles.data,
  friends: state.friends.data
}), {})(ArticlePage);
