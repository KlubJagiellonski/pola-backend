import React from 'react';
import { IArticle } from '../../domain/articles';
import { ArticleBlock } from './ArticleBlock';
import { ArticlesButton, Wrapper } from './ArticlesList.css';
import { ButtonColor} from '../buttons/Button';

interface IArticlesList {
  articles?: IArticle[];
}

export const ArticlesList: React.FC<IArticlesList> = ({ articles }) => {
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
          />
        ))}
      <ArticlesButton label="ZOBACZ POPRZEDNIE ARTYKUŁY" color={ButtonColor.Red} />
    </Wrapper>
  );
};

export default ArticlesList;
