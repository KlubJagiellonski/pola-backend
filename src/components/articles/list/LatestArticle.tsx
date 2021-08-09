import React from 'react'
import styled from 'styled-components'
import { color, padding, Device } from '../../../styles/theme';
import { ResponsiveImage } from '../../images/ResponsiveImage';
import ArticleContents from './ArticleContents';
import ArticleTitle from './ArticleTitle';

interface IArticleBlock {
  title: string;
  slug: string;
  photo?: string;
  date?: string;
  text: string;
  tag?: string;
}

const Wrapper = styled.div`
  height: 16em;
  position: relative;

  @media ${Device.mobile} {
    display: none;
  }
`

const Image = styled.div`
  div{
    height: 16em !important;

    picture {
    img{
      height: auto !important;
      }
    }
  }
`

const Sections = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 1;
  display: flex;
`

const ImageSection = styled(Image)`
  flex: 3;
`

const TextSection = styled.div`
  flex: 4;
  background: ${color.background.transparencyGrey};
  padding: ${padding.normal};
`

const LatestArticle: React.FC<IArticleBlock> = ({ photo, title, slug, date, text, tag }) => {
  return (
    <Wrapper>
      <Sections>
        <ImageSection>
          {photo && <ResponsiveImage imageSrc={photo} />}
        </ImageSection>
        <TextSection>
          <ArticleTitle title={title} slug={slug} tag={tag} date={date} />
          <ArticleContents
            date={date}
            text={text}
            tag={tag}
          />
        </TextSection>
      </Sections>
      <Image>
        {photo && <ResponsiveImage imageSrc={photo} />}
      </Image>
    </Wrapper>
  )
}

export default LatestArticle;