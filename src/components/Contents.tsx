import React, { useEffect, useState } from 'react';
import { Wrapper, LeftColumn, RightColumn, Column } from './Contents.css';
import DevelopmentSection from './DevelopmentSection';
import SocialMedia from './SocialMedia';
import { ArticlesList } from '../articles/components/ArticlesList';
import Friends from './Friends';
import Teams from './Teams';
import Download from './Download';
import About from './About';
import { color } from '../styles/theme';

const Contents = () => {
  //const [width, setWidth] = useState(window.innerWidth);

  // useEffect(() => {
  //   window.addEventListener('resize', handleResize);
  //   return () => window.removeEventListener('resize', handleResize);
  // }, []);

  // const handleResize = () => {
  //   setWidth(window.innerWidth);
  // };

  const bigView = (
    <Wrapper>
      <Column>
        <LeftColumn>
          <ArticlesList width={600} />
        </LeftColumn>
      </Column>
      <Column>
        <RightColumn>
          <DevelopmentSection />
          <SocialMedia />
          <About />
        </RightColumn>
      </Column>
      <Friends />
      <Column>
        <LeftColumn>
          <Teams
            title="Dołącz do Przyjaciół Poli i odnieś sukces!"
            text="Jedno zdanie, że sekcja jest kierowana do firm"
            buttonText="POZNAJ SZCZEGÓŁY"
          />
        </LeftColumn>
      </Column>
      <Column>
        <RightColumn>
          <Teams
            title="Zespół"
            text="1-2 zdania: ogólnie kto tworzy Polę (jaka grupa ludzi np. studenci, członkowie Klubu itp.)"
            buttonText="DOŁĄCZ DO ZESPOŁU"
          />
        </RightColumn>
      </Column>
      <Download />
    </Wrapper>
  );

  const smallView = (
    <Wrapper>
      <DevelopmentSection />
      <ArticlesList width={600} />
      <About />
      <SocialMedia />
      <Friends />
      <div style={{ background: color.primary, width: '100%' }}>
        <Teams
          title="Dołącz do Przyjaciół Poli i odnieś sukces!"
          text="Jedno zdanie, że sekcja jest kierowana do firm"
          buttonText="POZNAJ SZCZEGÓŁY"
        />
      </div>
      <Teams
        title="Zespół"
        text="1-2 zdania: ogólnie kto tworzy Polę (jaka grupa ludzi np. studenci, członkowie Klubu itp.)"
        buttonText="DOŁĄCZ DO ZESPOŁU"
      />
      <Download />
    </Wrapper>
  );

  return <>{600 <= 768 ? smallView : bigView}</>;
};

export default Contents;
