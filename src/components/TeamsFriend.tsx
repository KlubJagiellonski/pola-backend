import React from 'react';
import styled from 'styled-components'
import { WrapperTeams, Title, TextSection, ButtonTeams } from './Teams.css';
import { Text } from '../styles/GlobalStyle.css';
import { color, Device } from '../styles/theme';
import {ButtonColor } from './buttons/Button';

const Wrapper = styled(WrapperTeams)`
  grid-area: teams-friend;

  @media ${Device.mobile}{
    background-color: ${color.primary};
  }
`

const TeamsFriend = () => {
  return (
    <Wrapper color={color.primary}>
    <TextSection>
      <Title>Dołącz do Przyjaciół Poli i odnieś sukces!</Title>
      <Text>Jedno zdanie, że sekcja jest kierowana do firm</Text>
      <ButtonTeams label="POZNAJ SZCZEGÓŁY" color={ButtonColor.Red}/>
    </TextSection>
  </Wrapper>
  );
};

export default TeamsFriend;