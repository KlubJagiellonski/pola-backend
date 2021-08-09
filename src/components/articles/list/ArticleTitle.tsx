import React from 'react';
import styled from 'styled-components';
import { Link } from 'gatsby';
import { TitleSection, Text } from '../../../styles/GlobalStyle.css';
import { Device, fontSize, margin } from '../../../styles/theme';
import { getDate } from '../../../utils/dates';

const Wrapper = styled.div`
  margin-bottom: ${margin.normal};

  @media ${Device.mobile} {
    font-size: ${fontSize.small};
  }

`;

const Title = styled(TitleSection)`
  padding: 0;
  margin: 0;
`;

const ArticleLink = styled(Link)`
  text-decoration: none;
`

const TextInfo = styled(Text)`
    @media ${Device.desktop} {
    display: none;
  }
`

interface IArticleTitle {
  title: string;
  slug: string;
  tag?: string;
  date?: string;
}

const ArticleTitle: React.FC<IArticleTitle> = ({ title, slug, tag, date }) => {
  return (
    <Wrapper>
      <ArticleLink to={slug}>
        <Title>{title}</Title>
      </ArticleLink>
      {tag && date &&
        <TextInfo>{tag} | {getDate(date)}</TextInfo>
      }
    </Wrapper>
  )
}

export default ArticleTitle

