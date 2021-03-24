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

export const PageLayout = ({ children }: { children: any }) => {
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
      <div
        style={{
          margin: '0 auto',
          maxWidth: 960,
          padding: '0px 1.0875rem 1.45rem',
          paddingTop: 0,
        }}>
        <main>{children}</main>
      </div>
        <PageFooter />
    </LayoutContainer>
  );
};
