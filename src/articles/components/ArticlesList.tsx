import React from 'react';
import { ArticleBlock } from './ArticleBlock';
import { ArticlesButton, Wrapper } from './ArticlesList.css';
// import Photo from '../../assets/xmas.png';

const article = {
  photo: 'xmas.png',
  title: 'ŚWIĄTECZNE ZAKUPY Z POLA APP DO 15% TANIEJ',
  data: '12 grudnia 2021',
  text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
};

interface IArticlesList {
  width: number;
}

export const ArticlesList: React.FC<IArticlesList> = ({ width }) => {
  return (
    <Wrapper>
      <ArticleBlock photo={article.photo} title={article.title} date={article.data} text={article.text} width={600} />
      <ArticleBlock photo={article.photo} title={article.title} date={article.data} text={article.text} width={600} />
      <ArticleBlock photo={article.photo} title={article.title} date={article.data} text={article.text} width={600} />
      <ArticlesButton>CZYTAJ WIĘCEJ</ArticlesButton>
    </Wrapper>
  );
};

export default ArticlesList;
