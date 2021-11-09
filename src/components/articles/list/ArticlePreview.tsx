import React from 'react';
import styled from 'styled-components';
import styledContainerQuery from 'styled-container-query';
import { ResponsiveImage } from '../../images/ResponsiveImage';
import { Device, color, fontSize, margin } from '../../../styles/theme';
import ArticleContents from './ArticleContents';
import ArticleTitle from './ArticleTitle';
import { Article } from '../../../domain/articles';
import { ArticleDate, ArticleTag, ArticleText } from './ArticleContents.css';
import { Title } from './ArticleTitle';

const ArticleImage = styled.div`
  width: 50%;
  text-align: left;
  height: 100%;

  .gatsby-image-wrapper {
    div {
      padding-bottom: 100% !important;
    }
  }
`;

const Container = styledContainerQuery.div`
  display: flex;
  flex-direction: row;
  margin-bottom: 15px;

  @media ${Device.mobile} {
    min-height: 0;
  }

  &:container(max-width: 450px) {
    min-height: 0;

    ${ArticleTag} {
      display: none;
    }

    ${ArticleDate} {
      display: none;
    }

    ${ArticleText} {
      font-size: ${fontSize.tiny};
      -webkit-line-clamp: 3;
    }

    ${Title} {
      font-size: ${fontSize.tiny};
      -webkit-line-clamp: 2;
    }
  }
`;

const ArticleSection = styled.div`
  width: 50%;
  margin: 0 ${margin.normal};
  display: flex;
  flex-direction: column;

  @media ${Device.mobile} {
    width: 60%;
  }
`;

export const ArticlePreview: React.FC<Article> = ({ imagePath, title, slug, date, subTitle, tag }) => {
  return (
    <Container color={color.background.white}>
      <ArticleImage>{imagePath && <ResponsiveImage imageSrc={imagePath} />}</ArticleImage>
      <ArticleSection>
        <ArticleTitle title={title} slug={slug} />
        <ArticleContents date={date} text={subTitle} tag={tag} />
      </ArticleSection>
    </Container>
  );
};
