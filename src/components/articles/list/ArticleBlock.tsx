import React from 'react';
import styled from 'styled-components';
import { ResponsiveImage } from '../../images/ResponsiveImage';
import { WrapperSection } from '../../../styles/GlobalStyle.css';
import { Device, color } from '../../../styles/theme';
import ArticleContents from './ArticleContents';
import ArticleTitle from './ArticleTitle';

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

interface IArticleBlock {
  title: string;
  slug: string;
  photo?: string;
  date?: string;
  text: string;
  tag?: string;
}

export const ArticleBlock: React.FC<IArticleBlock> = ({ photo, title, slug, date, text, tag }) => {
  return (
    <Wrapper color={color.background.white}>
      <ArticleImage>{photo && <ResponsiveImage imageSrc={photo} />}</ArticleImage>
      <ArticleSection>
        <ArticleTitle title={title} slug={slug} />
        <ArticleContents
          date={date}
          text={text}
          lines={4}
          tag={tag}
        />
      </ArticleSection>
    </Wrapper>
  );
};
