import React from 'react';
import { Wrapper, Title, TextSection, ButtonTeams } from './Teams.css';
import { Text } from '../styles/GlobalStyle.css';
import { color } from '../styles/theme';

type TeamsProps = {
  title: string;
  text: string;
  buttonText: string;
};

const Teams = ({ title, text, buttonText }: TeamsProps) => {
  return (
    <Wrapper color={color.dark}>
      <TextSection>
        <Title>{title}</Title>
        <Text>{text}</Text>
        <ButtonTeams>{buttonText}</ButtonTeams>
      </TextSection>
    </Wrapper>
  );
};

export default Teams;
