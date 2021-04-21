import React from 'react';
import { IArticle } from '../../domain/articles';
import { ArticleBlock } from './ArticleBlock';
import { ArticlesButton, Wrapper } from './ArticlesList.css';

interface IArticlesList {
  articles?: IArticle[];
  width: number;
}

export const ArticlesList: React.FC<IArticlesList> = ({ articles, width }) => {
  return (
    <Wrapper>
      {articles &&
        articles.map((article: IArticle) => (
          <ArticleBlock
            key={article.id}
            photo={article.image}
            title={article.title}
            date={article.date}
            text={article.content}
            width={600}
          />
        ))}
      <ArticlesButton>CZYTAJ WIĘCEJ</ArticlesButton>
    </Wrapper>
  );
};

export default ArticlesList;
