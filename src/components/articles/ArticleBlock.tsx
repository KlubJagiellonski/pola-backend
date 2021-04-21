import React from 'react';
import { Wrapper, ArticleImage, ArticleSection, ArticleButton } from './ArticleBlock.css';
import { color } from '../../styles/theme';
import { TitleSection, Text } from '../../styles/GlobalStyle.css';
import { ResponsiveImage } from '../../components/responsive-image';

interface IArticleBlock {
  photo?: string;
  title: string;
  date?: string;
  text: string;
  width: number;
}

export const ArticleBlock: React.FC<IArticleBlock> = ({ photo, title, date, text, width }) => {
  return (
    <Wrapper color={color.primary}>
      <ArticleImage>{photo && <ResponsiveImage imageSrc={photo} />}</ArticleImage>
      <ArticleSection>
        <TitleSection>{title}</TitleSection>
        <Text>{text}</Text>
        {width > 768 && (
          <>
            {date && <Text>{date}</Text>}
            <ArticleButton>lorem ipsum</ArticleButton>
          </>
        )}
      </ArticleSection>
    </Wrapper>
  );
};
