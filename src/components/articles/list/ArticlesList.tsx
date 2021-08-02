import React from 'react';
import styled from 'styled-components';
import { Article } from '../../../domain/articles';
import { ArticleBlock } from './ArticleBlock';
import { Device } from '../../../styles/theme';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: 15px 30px;
    margin-bottom: 15px;
  }
`;

interface IArticlesList {
  articles?: Article[];
}

export const ArticlesList: React.FC<IArticlesList> = ({ articles }) => {
  return (
    <Wrapper>
      {articles &&
        articles.map((article: Article) => (
          <ArticleBlock
            key={article.id}
            title={article.title}
            slug={article.slug}
            photo={article.imagePath}
            date={article.date}
            text={article.subTitle}
            tag={article.tag}
          />
        ))}
    </Wrapper>
  );
};

export default ArticlesList;
