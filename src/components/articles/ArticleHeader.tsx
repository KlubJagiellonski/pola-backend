import React from 'react';
import styled from 'styled-components';
import { padding } from '../../styles/theme';
import { getDate } from '../../utils/dates';

const Header = styled.div`
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  padding: ${padding.big} 0;
`;

interface IArticleHeader {
  title: string;
  subTitle: string;
  date: string;
}

export const ArticleHeader: React.FC<IArticleHeader> = ({ title, subTitle, date }) => (
  <Header>
    <h1>{title}</h1>
    <h2>{subTitle}</h2>
    <div>{getDate(date)}</div>
  </Header>
);
