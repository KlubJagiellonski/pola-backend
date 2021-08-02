import React from 'react';
import styled from 'styled-components';
import { Article } from '../../../domain/articles';
import { ButtonColor} from '../../../styles/button-theme';
import {Device, padding} from '../../../styles/theme'
import {PrimaryButton } from '../../buttons/PrimaryButton';
import ArticlesList from './ArticlesList';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: ${padding.normal} 0;
  }
`;

const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  padding: ${padding.normal};
`;

interface IArticlesList {
  articles?: Article[];
}

export const ArticlesMainPage: React.FC<IArticlesList> = ({ articles }) => {
  return (
    <Wrapper>
      <ArticlesList articles={articles}/>
      <ArticlesButton label="ZOBACZ POPRZEDNIE ARTYKUŁY" color={ButtonColor.Red} />
    </Wrapper>
  );
};

export default ArticlesMainPage;