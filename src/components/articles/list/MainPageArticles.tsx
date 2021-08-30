import { Link } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { Article } from '../../../domain/articles';
import { urls } from '../../../domain/website';
import { ButtonColor } from '../../../styles/button-theme';
import { Device, padding, margin } from '../../../styles/theme'
import { PrimaryButton } from '../../buttons/PrimaryButton';
import ArticlesListPreview from './ArticlesListPrewiev';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: ${padding.normal} 0;
  }
`;

const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  padding: ${padding.normal};
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;

  @media ${Device.mobile}{
    width: calc(100% - 2 * ${margin.normal});
    margin: 0 ${margin.normal};
  }
`;

interface IArticlesList {
  articles?: Article[];
}

export const ArticlesMainPage: React.FC<IArticlesList> = ({ articles }) => {
  return (
    <Wrapper>
      <ArticlesListPreview articles={articles} />
      <Link to={urls.pola.news}>
        <ArticlesButton label="ZOBACZ POPRZEDNIE ARTYKUŁY" color={ButtonColor.Red} />
      </Link>
    </Wrapper>
  );
};

export default ArticlesMainPage;