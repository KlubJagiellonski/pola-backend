import React from 'react';
import { Wrapper} from './Contents.css';
import DevelopmentSection from './DevelopmentSection';
import SocialMedia from './SocialMedia';
import { ArticlesList } from '../components/articles/ArticlesList';
import Friends from './Friends';
import Teams from './Teams';
import Download from './Download';
import About from './About';
import { IArticle } from '../domain/articles';
import TeamsFriend from './TeamsFriend';
import { IFriend } from '../domain/friends';

interface IContent {
  articles?: IArticle[];
  friends?: IFriend[];
}

const Contents: React.FC<IContent> = ({ articles, friends }) => {

  return (
    <Wrapper>
    <ArticlesList articles={articles}/>
    <DevelopmentSection />
    <SocialMedia />
    <About />
    <Friends friends={friends}/> 
    <Teams/>
    <TeamsFriend/>
    <Download /> 
  </Wrapper>
  );
};

export default Contents;