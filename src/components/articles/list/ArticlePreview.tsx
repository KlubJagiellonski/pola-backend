import React from 'react';
import styled from 'styled-components';
import { ResponsiveImage } from '../../images/ResponsiveImage';
import { WrapperSection } from '../../../styles/GlobalStyle.css';
import { Device, color } from '../../../styles/theme';
import ArticleContents from './ArticleContents';
import ArticleTitle from './ArticleTitle';
import { Article } from '../../../domain/articles';

const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  min-height: 16.5em;
  margin-bottom: 15px;

  @media ${Device.mobile} {
    min-height: 0;
  }
`;

const ArticleImage = styled.div<{ img?: string }>`
  width: 50%;
  text-align: left;
`;

const ArticleSection = styled.div`
  width: 50%;
  margin: 0 15px;

  @media ${Device.mobile} {
    width: 60%;
  }
`;

export const ArticlePreview: React.FC<Article> = ({ imagePath, title, slug, date, subTitle, tag }) => {
  return (
    <Wrapper color={color.background.white}>
      <ArticleImage>{imagePath && <ResponsiveImage imageSrc={imagePath} />}</ArticleImage>
      <ArticleSection>
        <ArticleTitle title={title} slug={slug} />
        <ArticleContents
          date={date}
          text={subTitle}
          tag={tag}
        />
      </ArticleSection>
    </Wrapper>
  );
};
