import React from 'react';
import styled from 'styled-components';
import { getDate } from '../../utils/dates';
import Img, { FluidObject } from 'gatsby-image';
import { Text } from '../../styles/GlobalStyle.css';

const Title = styled.h1`
  padding: 0;
  margin: 0;
`

const Image = styled(Img)`
  max-height: 80vh;
`

interface IArticleHeader {
  title: string;
  subTitle: string;
  date: string;
  fluid: FluidObject | FluidObject[];
  category?: string
}

export const ArticleHeader: React.FC<IArticleHeader> = ({ title, subTitle, date, fluid, category }) => (
  <>
    <Title>{title}</Title>
    <Text>{category} | {getDate(date)}</Text>
    <p>{subTitle}</p>
    <Image fluid={fluid} />
  </>
);
