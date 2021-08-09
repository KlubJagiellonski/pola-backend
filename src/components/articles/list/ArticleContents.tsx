import React from 'react';
import styled from 'styled-components';
import { Text } from '../../../styles/GlobalStyle.css';
import { Device, fontSize, margin, color } from '../../../styles/theme';
import { getDate } from '../../../utils/dates';
import Tag from '../../tags/Tag';

const ArticleTag = styled.div`
  @media ${Device.desktop} {
    margin-top: ${margin.big};
  }

  @media ${Device.mobile} {
    display: none;
  }
`;

const ArticleDate = styled(Text)`
  color: ${color.text.red};

  @media ${Device.mobile} {
    display: none;
  }
`;

const ArticleText = styled(Text)`
   overflow: hidden;
   text-overflow: ellipsis;
   display: -webkit-box;
   -webkit-line-clamp: 4;
   -webkit-box-orient: vertical;

  @media ${Device.mobile} {
    font-size: ${fontSize.small};
  }
`;

interface IArticleContents {
  date?: string;
  text: string;
  tag?: String;
}

const ArticleContents: React.FC<IArticleContents> = ({ date, text, tag }) => {
  return (
    <>
      <ArticleText>{text}</ArticleText>
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
