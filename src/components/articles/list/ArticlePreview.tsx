import React from 'react';
import styled from 'styled-components';
import styledContainerQuery from 'styled-container-query'
import { ResponsiveImage } from '../../images/ResponsiveImage';
import { WrapperSection } from '../../../styles/GlobalStyle.css';
import { Device, color, fontSize } from '../../../styles/theme';
import ArticleContents from './ArticleContents';
import ArticleTitle from './ArticleTitle';
import { Article } from '../../../domain/articles';
import { ArticleDate, ArticleTag, ArticleText } from './ArticleContents.css';

const ArticleImage = styled.div`
  width: 50%;
  text-align: left;
  .gatsby-image-wrapper{
    div{
      padding-bottom: 14em !important;
    }
  }

  @media ${Device.mobile} {
    .gatsby-image-wrapper{
      div{
        padding-bottom: 5em !important;
      }
    }
  }
`;

const Wrapper = styled(WrapperSection)``;

const Container = styledContainerQuery.div`
  display: flex;
  flex-direction: row;
  min-height: 16.5em;
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
      font-size: ${fontSize.small};
    }

    ${ArticleImage}{
      .gatsby-image-wrapper{
        div{
          padding-bottom: 5em !important;
        }
      }
    }
  }
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
    <Container color={color.background.white}>
      <ArticleImage>{imagePath && <ResponsiveImage imageSrc={imagePath} />}</ArticleImage>
      <ArticleSection>
        <ArticleTitle title={title} slug={slug} />
        <ArticleContents
          date={date}
          text={subTitle}
          tag={tag}
        />
      </ArticleSection>
    </Container>
  );
};
