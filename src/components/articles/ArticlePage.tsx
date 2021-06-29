import React from 'react';
import styled from 'styled-components';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../../layout/PageLayout';
import SEOMetadata from '../../utils/browser/SEOMetadata';
import { IPolaState } from '../../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../../state/app/app-actions';
import { PageType } from '../../domain/website';
import { PageSection } from '../../layout/PageSection';
import { color } from '../../styles/theme';
import { ArticleHeader } from './ArticleHeader';
import { ArticleFooter } from './ArticleFooter';

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
  author?: any;
  slug?: string;
  facebook?: any;
}

const ArticlePage = (props: IArticlePage) => {
  const { location, article, author, slug, facebook } = props;
  const title = ((article || {}).frontmatter || {}).title;
  const subTitle = ((article || {}).frontmatter || {}).subTitle;
  const date = ((article || {}).fields || {}).prefix;
  const html = (article || {}).html;

  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.ARTICLE));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle={`Pola Web | ${title}`} />
      <PageSection size="full" styles={{ backgroundColor: color.background.secondary, textColor: color.text.dark }}>
        <ArticleHeader title={title} subTitle={subTitle} date={date} />
      </PageSection>
      <PageSection>
        <Content html={html} />
        <ArticleFooter slug={slug} author={author} facebook={facebook} />
      </PageSection>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({ location: state.app.location }), {})(ArticlePage);
