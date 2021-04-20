import React from 'react';
import Article from './Article';
import { ArticlesButton, Wrapper } from './Articles.css';
// import Photo from '../../assets/xmas.png';

const article = {
  photo: 'xmas.png',
  title: 'ŚWIĄTECZNE ZAKUPY Z POLA APP DO 15% TANIEJ',
  data: '12 grudnia 2021',
  text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
};

type ArticlesProps = {
  width: number;
};

export const Articles = ({ width }: ArticlesProps) => {
  return (
    <Wrapper>
      <Article photo={article.photo} title={article.title} date={article.data} text={article.text} width={600} />
      <Article photo={article.photo} title={article.title} date={article.data} text={article.text} width={600} />
      <Article photo={article.photo} title={article.title} date={article.data} text={article.text} width={600} />
      <ArticlesButton>CZYTAJ WIĘCEJ</ArticlesButton>
    </Wrapper>
  );
};

export default Articles;
