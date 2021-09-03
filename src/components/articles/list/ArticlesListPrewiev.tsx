import React from 'react';
import styled from 'styled-components';
import { Article } from '../../../domain/articles';
import { ArticlePreview } from './ArticlePreview';
import { Device, padding, margin } from '../../../styles/theme';
import { PrimaryButton } from '../../buttons/PrimaryButton';
import { Link } from 'gatsby';
import { urls } from '../../../domain/website';
import { ButtonColor } from '../../../styles/button-theme';

const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: ${padding.normal};
    margin-bottom: ${margin.normal};
  }
`;

const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  padding: ${padding.normal};
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
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
      <Link to={urls.pola.news}>
        <ArticlesButton label="ZOBACZ POPRZEDNIE ARTYKUŁY" color={ButtonColor.Red} />
      </Link>
    </Wrapper>
  );
};

export default ArticlesListPreview;
