import React from 'react';
import { getDate } from '../../../utils/dates';
import Tag from '../../tags/Tag';
import { ArticleDate, ArticleTag, ArticleText } from './ArticleContents.css';

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
