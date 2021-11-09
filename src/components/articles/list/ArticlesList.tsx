import React from 'react';
import styled from 'styled-components';
import { ArticleBlock } from './ArticleBlock';
import { Device, margin, padding } from '../../../styles/theme';
import { IArticlesTwoColumns } from './../../../utils/articles';

const Wrapper = styled.div`
  @media ${Device.mobile} {
    padding: ${padding.normal};
    margin-bottom: ${margin.normal};
    padding-top: 0;
    display: flex;
    flex-direction: column;
  }
`;

const Row = styled.div`
  display: flex;
  flex-direction: row;

  @media ${Device.mobile} {
    display: flex;
    flex-direction: column;
  }
`;

interface IArticlesList {
  articles?: IArticlesTwoColumns[];
}

export const ArticlesList: React.FC<IArticlesList> = ({ articles }) => {
  return (
    <Wrapper>
      {articles &&
        articles.map((article: IArticlesTwoColumns) => (
          <Row key={article.first.id}>
            <ArticleBlock
              id={article.first.id}
              title={article.first.title}
              slug={article.first.slug}
              imagePath={article.first.imagePath}
              date={article.first.date}
              subTitle={article.first.subTitle}
              tag={article.first.tag}
            />
            {article.second ? (
              <ArticleBlock
                id={article.second.id}
                title={article.second.title}
                slug={article.second.slug}
                imagePath={article.second.imagePath}
                date={article.second.date}
                subTitle={article.second.subTitle}
                tag={article.second.tag}
              />
            ) : (
              <div></div>
            )}
          </Row>
        ))}
    </Wrapper>
  );
};

export default ArticlesList;
