import React, { useEffect, useState } from 'react'
import styled from 'styled-components';
import { Article } from '../domain/articles';
import { Device, margin } from '../styles/theme';
import { getVisibleArticles } from '../utils/articles';
import { getTagsList } from '../utils/tags';
import ArticlesListPreview from './articles/list/ArticlesListPrewiev';
import DevelopmentSection from './DevelopmentSection';
import SocialMedia from './SocialMedia';
import TagsList from './tags/TagsList';

const Wrapper = styled.div`
  gap: ${margin.normal};
  display: flex;
  flex-direction: column;
`

const Title = styled.p`
  font-weight: bold;
`

const FirstSection = styled.div`
  @media ${Device.mobile} {
    display: none;
  }
`

const SecondSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${margin.normal};

  @media ${Device.mobile} {
    flex-direction: column-reverse;
  }
`

interface ISideInformations {
  actualArticleId: string,
  articles: Article[]
}

const SideInformations: React.FC<ISideInformations> = ({ actualArticleId, articles }) => {
  const [articlesPreview, setArticlesPreview] = useState<Article[]>([])

  useEffect(() => {
    if (articles) {
      setArticlesPreview(getVisibleArticles(actualArticleId, articles))
    }
  }, [articles]);

  return (
    <Wrapper>
      <FirstSection>
        <DevelopmentSection />
      </FirstSection>
      <SecondSection>
        <SocialMedia />
        <TagsList tag={articles && getTagsList(articles)} />
      </SecondSection>
      <Title>Zobacz także:</Title>
      <ArticlesListPreview articles={articlesPreview} />
    </Wrapper>
  )
}

export default SideInformations;