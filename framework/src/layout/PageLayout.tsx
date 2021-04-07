/*
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { useStaticQuery, graphql } from 'gatsby';

import { PageHeader } from './PageHeader';
import { PageFooter } from './PageFooter';
import './PageLayout.css';
import { todosRequested } from '../state/actions/todos';

const LayoutContainer = styled.div`
`;


const PageContent = styled.main`
  width: 100%;
  margin: 0 auto;
  padding: 0;
`;

export const PageLayout: React.FC = ({ children }) => {
  const dispatch = useDispatch();

  useEffect(() => {
    /*
     * This is an example of doing things when the app first loads.
     * You can dispatch a Redux action here to do some async thing
     * when the webapp boots up.
     */

    dispatch(todosRequested());
  }, []);

  const data = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
    }
  `);

  return (
    <LayoutContainer>
      <PageHeader siteTitle={data.site.siteMetadata.title} />
      <PageContent>
        {children}
      </PageContent>
        <PageFooter />
    </LayoutContainer>
  );
};
