import React, { useEffect, useState } from 'react';
import { Wrapper, LeftColumn, RightColumn, Column } from './Contents.css';
import DevelopmentSection from './DevelopmentSection';
import SocialMedia from './SocialMedia';
import Articles from './articles/Articles';
import Friends from './Friends';
import Teams from './Teams';
import Download from './Download';
import About from './About';
import { theme } from '../styles/theme';

const Contents = () => {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleResize = () => {
    setWidth(window.innerWidth);
  };

  const bigView = (
    <Wrapper>
      <Column>
        <LeftColumn>
          <Articles width={width} />
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
      <Articles width={width} />
      <About />
      <SocialMedia />
      <Friends />
      <div style={{ background: theme.primary, width: '100%' }}>
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

  return <>{width <= 768 ? smallView : bigView}</>;
};

export default Contents;
