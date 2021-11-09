import React from 'react';
import styled from 'styled-components';
import { ResponsiveImage } from '../../images/ResponsiveImage';
import { WrapperSection } from '../../../styles/GlobalStyle.css';
import { Device, color, margin, padding } from '../../../styles/theme';
import ArticleContents from './ArticleContents';
import ArticleTitle from './ArticleTitle';
import { PrimaryButton } from '../../buttons/PrimaryButton';
import { ButtonThemes, ButtonFlavor } from '../../../components/buttons/Button';
import { Link } from 'gatsby';
import { Article } from '../../../domain/articles';

const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  margin-bottom: ${margin.normal};

  @media ${Device.mobile} {
    min-height: 0;
    flex-direction: column-reverse;
  }
`;

const ArticleImage = styled.div<{ img?: string }>`
  width: 50%;
  text-align: left;

  .gatsby-image-wrapper {
    div {
      padding-bottom: 100% !important;
    }
  }

  @media ${Device.mobile} {
    width: 100%;
  }
`;

const ArticleSection = styled.div`
  width: 50%;
  margin: 0 ${margin.normal};
  display: flex;
  flex-direction: column;

  @media ${Device.mobile} {
    width: 100%;
    margin: ${margin.normal} 0;
  }
`;

const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  margin: ${margin.normal} 0;

  @media ${Device.desktop} {
    display: none;
  }
`;

const Contents = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;

  @media ${Device.mobile} {
    p:first-child {
      -webkit-line-clamp: 8;
    }
  }
`;

export const ArticleBlock: React.FC<Article> = ({ imagePath, title, slug, date, subTitle, tag }) => {
  return (
    <Wrapper color={color.background.white}>
      <Link to={slug}>
        <ArticlesButton label="CZYTAJ DALEJ" styles={ButtonThemes[ButtonFlavor.RED]} />
      </Link>
      <ArticleImage>{imagePath && <ResponsiveImage imageSrc={imagePath} />}</ArticleImage>
      <ArticleSection>
        <ArticleTitle title={title} slug={slug} tag={tag} date={date} />
        <Contents>
          <ArticleContents date={date} text={subTitle} tag={tag} />
        </Contents>
      </ArticleSection>
    </Wrapper>
  );
};
