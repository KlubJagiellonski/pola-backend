import React from 'react';
import styled from 'styled-components';
import { Link } from 'gatsby';
import { TitleSection } from '../../../styles/GlobalStyle.css';
import { Device, fontSize } from '../../../styles/theme';

const Title = styled(TitleSection)`
  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`;

const ArticleLink = styled(Link)`
  text-decoration: none;
`

interface IArticleTitle {
  title: string;
  slug: string;
}

const ArticleTitle: React.FC<IArticleTitle> = ({ title, slug }) => {
  return (
    <ArticleLink to={slug}>
      <Title>{title}</Title>
    </ArticleLink>
  )
}

export default ArticleTitle

