import React from 'react';
import styled from 'styled-components';
import { Article } from '../../../domain/articles';
import { ArticlePreview } from './ArticlePreview';
import { Device, padding, margin } from '../../../styles/theme';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: ${padding.normal};
    margin-bottom: ${margin.normal};
  }
`;

interface IArticlesList {
  articles?: Article[];
}

export const ArticlesListPreview: React.FC<IArticlesList> = ({ articles }) => {
  return (
    <Wrapper>
      {articles &&
        articles.map((article: Article) => (
          <ArticlePreview
            key={article.id}
            id={article.id}
            title={article.title}
            slug={article.slug}
            imagePath={article.imagePath}
            date={article.date}
            subTitle={article.subTitle}
            tag={article.tag}
          />
        ))}
    </Wrapper>
  );
};

export default ArticlesListPreview;
