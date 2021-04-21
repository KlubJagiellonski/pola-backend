import React from 'react';
import { Wrapper, ArticleImage, ArticleSection, ArticleButton } from './Article.css';
import { color } from '../../styles/theme';
import { TitleSection, Text } from '../../styles/GlobalStyle.css';
import { ResponsiveImage } from '../responsive-image';

type ArticleProps = {
  photo: string;
  title: string;
  date: string;
  text: string;
  width: number;
};

const Article = ({ photo, title, date, text, width }: ArticleProps) => {
  return (
    <Wrapper color={color.primary}>
      <ArticleImage>
        <ResponsiveImage imageSrc={photo} />
      </ArticleImage>
      <ArticleSection>
        <TitleSection>{title}</TitleSection>
        <Text>{text}</Text>
        {width > 768 && (
          <>
            <Text>{date}</Text>
            <ArticleButton>lorem ipsum</ArticleButton>
          </>
        )}
      </ArticleSection>
    </Wrapper>
  );
};

export default Article;
