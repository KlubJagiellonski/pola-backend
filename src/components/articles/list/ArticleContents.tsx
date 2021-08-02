import React from 'react';
import styled from 'styled-components';
import { Text } from '../../../styles/GlobalStyle.css';
import { Device, fontSize, margin, color } from '../../../styles/theme';
import { getDate } from '../../../utils/dates';
import Tag from '../../tags/Tag';

const ArticleTag = styled.div`
  margin-top: ${margin.big};
`;

const ArticleDate = styled(Text)`
  color: ${color.text.red};

  @media ${Device.mobile} {
    display: none;
  }
`;

const ArticleText = styled(Text) <{ lines?: number }>`
   overflow: hidden;
   text-overflow: ellipsis;
   display: -webkit-box;
   -webkit-line-clamp: ${(props) => props.lines};
   -webkit-box-orient: vertical;

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`;

interface IArticleContents {
  date?: string;
  text: string;
  lines?: number;
  tag?: String;
}

const ArticleContents: React.FC<IArticleContents> = ({ date, text, lines, tag }) => {
  return (
    <>
      <ArticleText lines={lines}>{text}</ArticleText>
      {date && <ArticleDate>{getDate(date)}</ArticleDate>}
      {tag &&
        <ArticleTag>
          <Tag label={`${tag}`} />
        </ArticleTag>
      }
    </>
  );
};

export default ArticleContents
