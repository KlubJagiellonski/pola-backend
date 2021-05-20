import React from 'react';
import { Wrapper, Title, TextSection, ButtonTeams } from './Teams.css';
import { Text } from '../styles/GlobalStyle.css';
import { color } from '../styles/theme';
import {ButtonColor } from './buttons/Button';

const Teams = () => {
  return (
    <Wrapper color={color.primary}>
      <TextSection>
        <Title>Zespół</Title>
        <Text>1-2 zdania: ogólnie kto tworzy Polę (jaka grupa ludzi np. studenci, członkowie Klubu itp.)</Text>
        <ButtonTeams label="DOŁĄCZ DO ZESPOŁU" color={ButtonColor.Red}/>
      </TextSection>
    </Wrapper>
  );
};

export default Teams;
