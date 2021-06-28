import React from 'react';
import styled from 'styled-components';
import { Article } from '../../../domain/articles';
import { ArticleBlock } from './ArticleBlock';
import { ButtonColor } from '../../../styles/button-theme';
import { Device, padding } from '../../../styles/theme';
import { PrimaryButton } from '../../buttons/PrimaryButton';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: 15px 30px;
    margin-bottom: 15px;
  }
`;

const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  padding: ${padding.normal};
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
          />
        ))}
      <ArticlesButton label="ZOBACZ POPRZEDNIE ARTYKUŁY" color={ButtonColor.Red} />
    </Wrapper>
  );
};

export default ArticlesList;
