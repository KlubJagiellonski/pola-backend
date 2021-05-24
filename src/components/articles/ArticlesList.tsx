import React from 'react';
import styled from 'styled-components';
import { IArticle } from '../../domain/articles';
import { ArticleBlock } from './ArticleBlock';
import { ButtonColor} from '../buttons/Button';
import {Device, padding} from './../../styles/theme'
import {PrimaryButton } from '../buttons/PrimaryButton';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: 15px 30px;
    margin-bottom: 15px;
  }
`;

const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  padding: ${padding.normal}
`;

interface IArticlesList {
  articles?: IArticle[];
}

export const ArticlesList: React.FC<IArticlesList> = ({ articles }) => {
  return (
    <Wrapper>
      {articles &&
        articles.map((article: IArticle) => (
          <ArticleBlock
            key={article.id}
            photo={article.image}
            title={article.title}
            date={article.date}
            text={article.content}
          />
        ))}
      <ArticlesButton label="ZOBACZ POPRZEDNIE ARTYKUŁY" color={ButtonColor.Red} />
    </Wrapper>
  );
};

export default ArticlesList;
