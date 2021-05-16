import React from 'react';
import { Wrapper, Title, TextSection, ButtonTeams } from './Teams.css';
import { Text } from '../styles/GlobalStyle.css';
import { color } from '../styles/theme';

const Teams = () => {
  return (
    <Wrapper color={color.secondary}>
      <TextSection>
        <Title>Zespół</Title>
        <Text>1-2 zdania: ogólnie kto tworzy Polę (jaka grupa ludzi np. studenci, członkowie Klubu itp.)</Text>
        <ButtonTeams>DOŁĄCZ DO ZESPOŁU</ButtonTeams>
      </TextSection>
    </Wrapper>
  );
};

export default Teams;
