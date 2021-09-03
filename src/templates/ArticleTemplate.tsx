import React from 'react';
import ArticlePage from '../components/articles/ArticlePage';
import { graphql } from 'gatsby';

interface IArticleTemplate {
  data: any;
  pageContext: any;
}

export const ArticleTemplate: React.FC<IArticleTemplate> = ({ data, pageContext }) => (
  <ArticlePage article={data.post} slug={pageContext.slug as string} />
);

export default ArticleTemplate;

//eslint-disable-next-line no-undef
export const postQuery = graphql`
  query PostBySlug($slug: String!) {
    post: markdownRemark(fields: { slug: { eq: $slug } }) {
      id
      html
      htmlAst
      fields {
        slug
        prefix
      }
      frontmatter {
        title
        subTitle
        category
        cover {
          childImageSharp {
            fluid {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    }
  }
`;
