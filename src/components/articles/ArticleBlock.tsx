import React from 'react';
import { Wrapper, ArticleImage, ArticleSection, ArticleButton, ArticleDate } from './ArticleBlock.css';
import { color } from '../../styles/theme';
import { TitleSection, Text } from '../../styles/GlobalStyle.css';
import { ResponsiveImage } from '../../components/responsive-image';
import {ButtonColor} from './../buttons/Button'

interface IArticleBlock {
  photo?: string;
  title: string;
  date?: string;
  text: string;
}

export const ArticleBlock: React.FC<IArticleBlock> = ({ photo, title, date, text}) => {
  return (
    <Wrapper color={color.primary}>
      <ArticleImage>{photo && <ResponsiveImage imageSrc={photo} />}</ArticleImage>
      <ArticleSection>
        <TitleSection>{title}</TitleSection>
        <Text>{text}</Text>
        {date && <ArticleDate>{date}</ArticleDate>}
        <ArticleButton label='TAG/KATEGORIA' color={ButtonColor.LightGray}/>
      </ArticleSection>
    </Wrapper>
  );
};
